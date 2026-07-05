# Expense Manager

A personal finance web application built with Flask that helps users understand where their money goes by tracking income, expenses, and monthly budgets.

This project is being developed as my CS50 Final Project, but the long-term goal is to evolve it into a polished portfolio project with more advanced analytics and automation.

---

## Motivation

Many expense trackers focus only on recording transactions. This project aims to answer a more useful question:

> **"Where is my money actually going?"**

The emphasis is on helping users understand their spending habits through a clean dashboard, category-based budgeting, and meaningful summaries rather than simply storing financial records.

---

## Features

### User Authentication

- Register a new account
- Secure login
- Logout

### Transactions

- Record income
- Record expenses
- Edit transactions
- Delete transactions
- View transaction history

### Budget Management

- Set monthly budgets by category
- Compare spending against budgets
- Track remaining budget for each category

### Dashboard

- Monthly income summary
- Monthly expense summary
- Remaining balance
- Spending by category
- Budget progress
- Recent transactions

---

## Tech Stack

### Backend

- Python
- Flask
- SQLite

### Frontend

- HTML
- CSS
- Bootstrap 5
- Jinja2

### Development Tools

- Git
- GitHub
- VS Code

---

## Database

The application uses SQLite with a normalized relational database.

Current tables include:

- Users
- Categories
- Transactions
- Budgets

### Design Decisions

- Money is stored as **INTEGER (paise)** instead of floating-point values to avoid precision issues.
- Categories are predefined for Version 1.
- Budgets are stored monthly and enforced using composite unique constraints.
- SQLite foreign key support is enabled for every database connection.

---

## Current Status

🚧 Work in Progress

Completed:

- Project setup
- SQLite database schema
- Base application layout
- Responsive navigation
- Flash messaging
- Design system

Currently working on:

- User authentication

---

## Future Improvements

After completing the CS50 project, planned improvements include:

- CSV bank statement import
- Automatic transaction categorization
- Recurring transaction detection
- Spending analytics
- Budget insights
- Spending anomaly detection
- Improved dashboard visualizations
- Native iOS application built with Swift

---

## Screenshots

Screenshots will be added as the project develops.

---

## Learning Goals

This project is intentionally built without SQLAlchemy to strengthen my understanding of:

- SQL
- Relational database design
- SQLite
- Flask
- Jinja templating
- Authentication
- Software architecture
- Git workflows

The focus is on understanding the underlying technologies before introducing higher-level abstractions.

---

## Installation

```bash
git clone <repository-url>

cd expense-manager

python -m venv .venv

# Activate virtual environment

pip install -r requirements.txt

python init_db.py

flask run
```

---

## License

This project is currently intended for educational and portfolio purposes.