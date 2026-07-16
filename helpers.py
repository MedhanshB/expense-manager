import sqlite3
from flask import session, redirect
from functools import wraps
from datetime import datetime

def get_db():
    conn = sqlite3.connect("expense_manager.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def inr(amount):
    """Format a value stored in paise as Indian Rupees."""
    amount = amount / 100
    return f"₹{amount:,.2f}"

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def short_date(date):
    short = datetime.strptime(date, "%Y-%m-%d")
    short_date = short.strftime("%d %b")
    return short_date

def get_budget_summary(user_id):
    db = get_db()

    current_month = datetime.now().strftime("%Y-%m")

    cursor = db.execute(
        """
        SELECT
            budgets.id,
            budgets.category_id,
            budgets.budget_amount,
            budgets.budget_period,
            categories.name
        FROM budgets
        INNER JOIN categories
            ON budgets.category_id = categories.id
        WHERE budgets.user_id = ?
        """,
        (user_id,))
    
    budgets_data = cursor.fetchall()

    cursor = db.execute(
        """
        SELECT 
            categories.id AS category_id,
        SUM (transactions.amount) AS total
        FROM transactions
        INNER JOIN categories
            ON transactions.category_id = categories.id
        WHERE transactions.user_id = ? AND categories.type = ? AND strftime("%Y-%m", transactions.transaction_date = ?)
        GROUP BY categories.id
        """,
        (user_id, "Expense", current_month))
    
    transactions_data = cursor.fetchall()

    spent = {}

    budget_summary = []

    for transaction in transactions_data:
        spent[transaction["category_id"]] = transaction["total"]

    for budget in budgets_data:
        spent_amount = spent.get(budget["category_id"], 0)
        remaining_amount = budget["budget_amount"] - spent_amount
        if budget["budget_amount"] > 0:
            progress = spent_amount / budget["budget_amount"] * 100
        else:
            progress = 0

        budget_summary.append({
            "id":budget["id"],
            "name": budget["name"],
            "budget_amount": budget["budget_amount"],
            "spent": spent_amount,
            "remaining": remaining_amount,
            "progress": progress
        })

    return budget_summary