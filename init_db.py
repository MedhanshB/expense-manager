import sqlite3

with sqlite3.connect("expense.db") as conn:
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())

print("Database initialized successfully.")