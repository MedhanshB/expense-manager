import sqlite3
from flask import session, redirect, current_app
from functools import wraps
from datetime import date
import psycopg
import os 
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()


def get_db():
    return psycopg.connect(
        os.getenv("DATABASE_URL"),
        row_factory=dict_row
    )


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

def short_date(value):
    return value.strftime("%d %b")

def month_range(year, month):
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)

    return start, end
    

def current_month_range():
    today = date.today()
    return month_range(today.year, today.month)


def get_budget_summary(user_id, year, month):
    start, end = month_range(year, month)
    with get_db() as db:

        cursor = db.execute(
            """
            SELECT
                budgets.id,
                budgets.category_id,
                budgets.budget_amount,
                categories.name
            FROM budgets
            INNER JOIN categories
                ON budgets.category_id = categories.id
            WHERE budgets.user_id = %s
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
            WHERE
                transactions.user_id = %s
                AND categories.type = %s
                AND transactions.transaction_date >= %s
                AND transactions.transaction_date < %s
            GROUP BY categories.id
            """,
            (user_id, "Expense", start, end))
        
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
        
        progress = round(progress, 1)

        budget_summary.append({
            "id":budget["id"],
            "name": budget["name"],
            "budget_amount": budget["budget_amount"],
            "spent": spent_amount,
            "remaining": remaining_amount,
            "progress": progress
        })

    return budget_summary

def monthly_report(user_id, year, month):
    
    with get_db() as db:
        start,end = month_range(year, month)

        cursor = db.execute(
            """
                SELECT categories.id as categories_id, categories.name,
                SUM (transactions.amount) as total
                FROM transactions  
                INNER JOIN categories
                    ON transactions.category_id = categories.id
                WHERE
                    transactions.user_id = %s
                    AND categories.type = %s
                    AND transactions.transaction_date >= %s
                    AND transactions.transaction_date < %s
                GROUP BY categories.id, categories.name
                ORDER BY total DESC;
                """,
                (user_id, "Expense", start, end))
        
        expenses = cursor.fetchall()

        cursor = db.execute(
            """
                SELECT categories.id as categories_id, categories.name,
                SUM (transactions.amount) as total
                FROM transactions  
                INNER JOIN categories
                    ON transactions.category_id = categories.id
                WHERE
                    transactions.user_id = %s
                    AND categories.type = %s
                    AND transactions.transaction_date >= %s
                    AND transactions.transaction_date < %s
                GROUP BY categories.id, categories.name
                ORDER BY total DESC;
                """,
                (user_id, "Income", start, end))
        
        income = cursor.fetchall()

        budget = get_budget_summary(user_id, year, month)

        total_expenses = sum(row["total"] for row in expenses)

        total_income = sum(row["total"] for row in income)

        net_income = total_income - total_expenses

        report = {
            "expenses": expenses,
            "income": income,
            "budgets": budget,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_income": net_income
        }

        return report