import sqlite3
from flask import session, redirect
from functools import wraps

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