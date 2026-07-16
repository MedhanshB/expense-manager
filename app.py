from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from helpers import get_db, login_required, inr, short_date, get_budget_summary

app = Flask(__name__)

app.config["SECRET_KEY"] = "development-key"   # replace later with an environment variable

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

MAX_TRANSACTION_AMOUNT = Decimal("10000000")

Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.jinja_env.filters["inr"] = inr
app.jinja_env.filters["short_date"] = short_date



@app.route("/")
@login_required
def index():

    user_id = session["user_id"]

    db = get_db()

    # cursor = db.execute(
    # """
    # SELECT
    #     transactions.amount,
    #     categories.type
    # FROM transactions
    # INNER JOIN categories
    #     ON transactions.category_id = categories.id
    # WHERE transactions.user_id = ?
    # """,
    # (user_id,)
    # )

    # transactions = cursor.fetchall()

        # cursor = db.execute(
    # """
    # SELECT SUM(transactions.amount) AS total_income
    # FROM transactions 
    # INNER JOIN categories 
    #     ON transactions.category_id = categories.id
    # WHERE 
    #     transactions.user_id = ? 
    #     AND categories.type = ?
    # """,
    # (user_id,'Income')
    # )
    
    # row = cursor.fetchone()
    # user_income = row["total_income"]

    # cursor = db.execute(
    # """
    # SELECT SUM(transactions.amount) AS total_expense
    # FROM transactions 
    # INNER JOIN categories 
    #     ON transactions.category_id = categories.id
    # WHERE 
    #     transactions.user_id = ? 
    #     AND categories.type = ?
    # """,
    # (user_id,'Expense')
    # )

    # row2 = cursor.fetchone()
    # user_expense = row2["total_expense"]

    # for transaction in transactions:
    #     if transaction["type"] == "Income":
    #         user_income += transaction["amount"]
    #     else:
    #         user_expense += transaction["amount"]

    cursor = db.execute(
    """
    SELECT categories.type,
        SUM(transactions.amount) AS total
    FROM transactions
    INNER JOIN categories
        ON transactions.category_id = categories.id
    WHERE
        transactions.user_id = ? 
    GROUP BY categories.type
    """,
    (user_id,)
    )

    balance = cursor.fetchall()

    user_income = 0
    user_expense = 0

    for balances in balance:
        if balances["type"] == "Income":
            user_income = balances["total"]
        elif balances["type"] == "Expense":
            user_expense = balances["total"]

    user_balance = user_income - user_expense

    cursor = db.execute(
    """
    SELECT
        transactions.id,
        categories.name,
        categories.type,
        transactions.amount,
        transactions.description,
        transactions.transaction_date
    FROM transactions
    INNER JOIN categories
        ON transactions.category_id = categories.id
    WHERE transactions.user_id = ?
    ORDER BY transactions.transaction_date DESC, transactions.id DESC
    LIMIT 10
    """, (user_id,))

    transactions = cursor.fetchall()

    budget_summary = get_budget_summary(user_id)


    return render_template("index.html", balance = user_balance, income = user_income, expense = user_expense, 
                           transactions = transactions, budgets = budget_summary)

    


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        if not username:
            flash("must provide username","danger")
            return redirect(url_for("register"))

        password = request.form.get("password")
        if not password:
            flash("must provide password","danger")
            return redirect(url_for("register"))
        confPass = request.form.get("confirm_password")
        if not confPass:
            flash("must provide the confirm password","danger")
            return redirect(url_for("register"))
        if confPass != password:
            flash("must match the password","danger")
            return redirect(url_for("register"))


        db = get_db()

        cursor_user = db.execute("SELECT username FROM users WHERE username=?", (username,))
        users = cursor_user.fetchone()
        if users:
            flash("Username already exists", "danger")
            db.close()
            return redirect(url_for("register"))
        
        hashPass = generate_password_hash(password)

        db.execute("INSERT INTO users (username, password_hash) VALUES(?, ?)", (username, hashPass))
        db.commit()

        db.close()

        flash("Registration successful! Please log in.", "success")

        return redirect(url_for("login"))
    

    else:
        return render_template("register.html")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    # no caching forget any user id 
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            flash("must provide username","danger")
            return redirect(url_for("login"))
        password = request.form.get("password")
        if not password:
            flash("must provide password","danger")
            return redirect(url_for("login"))

        db = get_db()

        cursor_user = db.execute("SELECT * FROM users WHERE username = ?", (username,))

        user = cursor_user.fetchone()
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid username or password","danger")
            return redirect(url_for("login"))

        session["user_id"] = user["id"]
        session["username"] = user["username"]

        db.close()

        flash("Welcome back!", "success")
        return redirect(url_for("index"))
        
    
    else:
        return render_template("login.html")
    

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    flash("Logged out!", "info")
    # Redirect user to login form
    return redirect(url_for("login"))


@app.route("/transactions")
@login_required
def transactions():
    user_id = session["user_id"]

    db = get_db()

    cursor = db.execute(
    """
    SELECT
        transactions.id,
        categories.name,
        transactions.amount,
        transactions.description,
        transactions.transaction_date
    FROM transactions
    INNER JOIN categories
        ON transactions.category_id = categories.id
    WHERE transactions.user_id = ?
    ORDER BY transactions.transaction_date DESC
    """, (user_id,))

    transactions_data = cursor.fetchall()



    return render_template("transactions.html", transactions_data = transactions_data)


@app.route("/transactions/add", methods=["GET", "POST"])
@login_required
def add_transaction():

    user_id = session["user_id"]

    db = get_db()

    cursor = db.execute("SELECT id,name FROM categories ORDER BY name")

    categories = cursor.fetchall()

    db.close()

    today = date.today().isoformat()


    if request.method == "POST":
        category = request.form.get("category")
        if not category:
            flash("Please select a category","danger")
            return render_template("add_transaction.html", categories = categories, today = today)

        amount = request.form.get("amount","").strip()
        if not amount:
            flash("Please enter an amount","danger")
            return render_template("add_transaction.html", categories = categories, today = today)
        try:
            amount = Decimal(amount)
        except InvalidOperation:
            flash("Enter a valid amount","danger")
            return render_template("add_transaction.html", categories = categories, today = today)
        
        exponent = amount.as_tuple().exponent

        if exponent < -2:
            flash("Amount can have at most two decimal places", "danger")
            return render_template("add_transaction.html", categories = categories, today = today)

        if amount <= 0:
            flash("Enter a valid amount","danger")
            return render_template("add_transaction.html", categories = categories, today = today)
        
        if amount > MAX_TRANSACTION_AMOUNT:
            flash("Amount seems unreasonably large", "danger")
            return render_template("add_transaction.html", categories = categories, today = today)
        
        description = request.form.get("description","").strip()
        if not description:
            flash("Please enter a description","danger")
            return render_template("add_transaction.html", categories = categories, today = today)
        
        transaction_date = request.form.get("date", "")
        try:
            date.fromisoformat(transaction_date)
        except (ValueError, TypeError):
            flash("Enter a valid date", "danger")
            return render_template("add_transaction.html", categories = categories, today = today)
        
        amount = amount * 100
        amount = int(amount)

        try:
            category = int(category)
        except ValueError:
            flash("Invalid category","danger")
            return render_template("add_transaction.html", categories = categories, today = today)

        db = get_db()
        cursor = db.execute("SELECT id FROM categories WHERE id=?",(category,))
        category_row = cursor.fetchone()
        if not category_row:
            db.close()
            flash("Not a valid category","info")
            return render_template("add_transaction.html", categories = categories, today = today)
        
 
        
        db.execute("INSERT INTO transactions (user_id, category_id,amount,description,transaction_date) VALUES(?, ?, ?, ?, ?)", 
                   (user_id, category, amount, description, transaction_date))
        
        db.commit()

        db.close()

        flash("Transaction saved successfully","success")
        
        return redirect(url_for("transactions"))


    else:

        return render_template("add_transaction.html", categories=categories, today=today)
    

@app.route("/transactions/<int:transaction_id>/edit", methods=["GET", "POST"])
@login_required
def edit_transaction(transaction_id):

    user_id = session["user_id"]

    if request.method == "POST":
        category = request.form.get("category")
        if not category:
            flash("Please select a category","danger")
            return render_template("edit_transaction.html", categories = categories)

        amount = request.form.get("amount","").strip()
        if not amount:
            flash("Please enter an amount","danger")
            return render_template("edit_transaction.html", categories = categories)
        try:
            amount = Decimal(amount)
        except InvalidOperation:
            flash("Enter a valid amount","danger")
            return render_template("edit_transaction.html", categories = categories)
        
        exponent = amount.as_tuple().exponent

        if exponent < -2:
            flash("Amount can have at most two decimal places", "danger")
            return render_template("edit_transaction.html", categories = categories)

        if amount <= 0:
            flash("Enter a valid amount","danger")
            return render_template("edit_transaction.html", categories = categories)
        
        if amount > MAX_TRANSACTION_AMOUNT:
            flash("Amount seems unreasonably large", "danger")
            return render_template("edit_transaction.html", categories = categories)
        
        description = request.form.get("description","").strip()
        if not description:
            flash("Please enter a description","danger")
            return render_template("edit_transaction.html", categories = categories)
        
        transaction_date = request.form.get("date", "")
        try:
            date.fromisoformat(transaction_date)
        except (ValueError, TypeError):
            flash("Enter a valid date", "danger")
            return render_template("edit_transaction.html", categories = categories)
        
        amount = amount * 100
        amount = int(amount)

        try:
            category = int(category)
        except ValueError:
            flash("Invalid category","danger")
            return render_template("edit_transaction.html", categories = categories)

        db = get_db()
        cursor = db.execute("SELECT id FROM categories WHERE id=?",(category,))
        category_row = cursor.fetchone()
        if not category_row:
            db.close()
            flash("Not a valid category","info")
            return render_template("edit_transaction.html", categories = categories)
        
 
        
        cursor_2 = db.execute("UPDATE transactions SET category_id = ?, amount = ?, description = ?, transaction_date = ? WHERE transactions.id = ? AND transactions.user_id=?", 
                   (category, amount, description, transaction_date, transaction_id, user_id))
        
        if cursor_2.rowcount == 0:
            db.rollback()
            db.close()
            flash("Transaction not found.", "danger")
            return redirect(url_for("transactions"))
        
        db.commit()

        db.close()

        flash("Transaction updated","success")
        
        return redirect(url_for("transactions"))
    
    else:
        
        db = get_db()

        cursor = db.execute(
        """
        SELECT
            transactions.category_id,
            categories.name,
            transactions.amount,
            transactions.description,
            transactions.transaction_date
        FROM transactions
        INNER JOIN categories
            ON transactions.category_id = categories.id
        WHERE transactions.id = ? AND transactions.user_id = ?
        """, (transaction_id, user_id))

        transaction = cursor.fetchone()
        
        if not transaction:
            db.close()
            flash("No transaction exists","danger")
            return redirect(url_for("transactions"))
        
        transaction = dict(transaction)
        
        transaction["amount"] = Decimal(transaction["amount"]) / 100

        cursor = db.execute("SELECT id,name FROM categories ORDER BY name")

        categories = cursor.fetchall()

        db.close()

        return render_template("edit_transaction.html", transaction = transaction, categories = categories)
    

@app.route("/transactions/<int:transaction_id>/delete", methods=["POST"])
@login_required
def delete_transaction(transaction_id):
    user_id = session["user_id"]

    db = get_db()

    cursor = db.execute(
        "DELETE FROM transactions WHERE transactions.user_id = ? AND transactions.id = ?",
        (user_id, transaction_id))

    if cursor.rowcount == 0:
            db.rollback()
            db.close()
            flash("Transaction not found.", "danger")
            return redirect(url_for("transactions"))

    db.commit()

    db.close()

    flash("Transaction deleted successfully.","success")
    return redirect(url_for("transactions"))


@app.route("/budgets")
@login_required
def budgets():
    user_id = session["user_id"]

    db = get_db()

    budget_summary = get_budget_summary(user_id)


    return render_template("budgets.html", budget_data = budget_summary)

        

    

@app.route("/budgets/add", methods=["GET", "POST"])
@login_required
def add_budget():

    user_id = session["user_id"]

    budget_period = datetime.now().strftime("%Y-%m")

    db = get_db()

    cursor = db.execute("SELECT id,name FROM categories WHERE type = ? ORDER BY name", ("Expense",))

    categories = cursor.fetchall()

    db.close()

    if request.method == "POST":
        category = request.form.get("category")
        if not category:
            flash("Please select a category","danger")
            return render_template("add_budget.html", categories = categories)

        budget = request.form.get("budget","").strip()
        if not budget:
            flash("Please enter an budget","danger")
            return render_template("add_budget.html", categories = categories)
        try:
            budget = Decimal(budget)
        except InvalidOperation:
            flash("Enter a valid budget","danger")
            return render_template("add_budget.html", categories = categories)
        
        exponent = budget.as_tuple().exponent

        if exponent < -2:
            flash("Amount can have at most two decimal places", "danger")
            return render_template("add_budget.html", categories = categories)

        if budget <= 0:
            flash("Enter a valid budget","danger")
            return render_template("add_budget.html", categories = categories)
        
        if budget > MAX_TRANSACTION_AMOUNT:
            flash("Amount seems unreasonably large", "danger")
            return render_template("add_budget.html", categories = categories)
        
        budget = budget * 100
        budget = int(budget)

        try:
            category = int(category)
        except ValueError:
            flash("Invalid category","danger")
            return render_template("add_budget.html", categories = categories)

        db = get_db()
        cursor = db.execute("SELECT id FROM categories WHERE id=? and type = ?",(category,"Expense"))
        category_row = cursor.fetchone()
        if not category_row:
            db.close()
            flash("Not a valid category","info")
            return render_template("add_budget.html", categories = categories)

        
        cursor = db.execute(
            """
            INSERT INTO budgets (user_id, category_id, budget_amount, budget_period) VALUES (?, ?, ?, ?)
            """,
            (user_id, category, budget, budget_period)
        )

        db.commit()

        db.close()
         
        return redirect(url_for("budgets"))
        

    else:

        return render_template("add_budget.html", categories=categories)



@app.route("/budgets/<int:budget_id>/edit", methods=["GET", "POST"])
@login_required
def edit_budget(budget_id):

    user_id = session["user_id"]

    if request.method == "POST":
        category = request.form.get("category")
        if not category:
            flash("Please select a category","danger")
            return render_template("edit_budget.html", categories = categories)

        budget = request.form.get("budget","").strip()
        if not budget:
            flash("Please enter an budget","danger")
            return render_template("edit_budget.html", categories = categories)
        try:
            budget = Decimal(budget)
        except InvalidOperation:
            flash("Enter a valid budget","danger")
            return render_template("edit_budget.html", categories = categories)
        
        exponent = budget.as_tuple().exponent

        if exponent < -2:
            flash("Amount can have at most two decimal places", "danger")
            return render_template("edit_budget.html", categories = categories)

        if budget <= 0:
            flash("Enter a valid budget","danger")
            return render_template("edit_budget.html", categories = categories)
        
        if budget > MAX_TRANSACTION_AMOUNT:
            flash("Amount seems unreasonably large", "danger")
            return render_template("edit_budget.html", categories = categories)
        
        budget = budget * 100
        budget = int(budget)

        try:
            category = int(category)
        except ValueError:
            flash("Invalid category","danger")
            return render_template("edit_budget.html", categories = categories)

        db = get_db()
        cursor = db.execute("SELECT id FROM categories WHERE id=?",(category,))
        category_row = cursor.fetchone()
        if not category_row:
            db.close()
            flash("Not a valid category","info")
            return render_template("edit_budget.html", categories = categories)
        
 
        
        cursor_2 = db.execute("UPDATE budgets SET category_id = ?, budget_amount = ? WHERE budget.id = ? AND budget.user_id=?", 
                   (category, budget, budget_id, user_id))
        
        if cursor_2.rowcount == 0:
            db.rollback()
            db.close()
            flash("Budget not found.", "danger")
            return redirect(url_for("budgets"))
        
        db.commit()

        db.close()

        flash("Budget updated","success")
        
        return redirect(url_for("budgets"))
    
    else:
        
        db = get_db()

        cursor = db.execute(
        """
        SELECT
            budgets.category_id,
            categories.name,
            budgets.budget_amount
        FROM budgets
        INNER JOIN categories
            ON budgets.category_id = categories.id
        WHERE budgets.id = ? AND budgets.user_id = ?
        """, (budget_id, user_id))

        budgets = cursor.fetchone()
        
        if not budgets:
            db.close()
            flash("No budget exists","danger")
            return redirect(url_for("budgets"))
        
        budgets = dict(budgets)
        
        budgets["budget_amount"] = Decimal(budgets["budget_amount"]) / 100

        cursor = db.execute("SELECT id,name FROM categories ORDER BY name")

        categories = cursor.fetchall()

        db.close()

        return render_template("edit_budget.html", budgets = budgets, categories = categories)


@app.route("/budgets/<int:budget_id>/delete", methods=["POST"])
@login_required
def delete_budget(budget_id):
    user_id = session["user_id"]

    db = get_db()

    cursor = db.execute(
        "DELETE FROM budgets WHERE budgets.user_id = ? AND budgets.id = ?",
        (user_id, budget_id))

    if cursor.rowcount == 0:
            db.rollback()
            db.close()
            flash("Budget not found.", "danger")
            return redirect(url_for("budgets"))

    db.commit()

    db.close()

    flash("Budget deleted successfully.","success")
    return redirect(url_for("budgets"))