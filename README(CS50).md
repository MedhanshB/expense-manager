# Expense Manager

#### Video Demo: https://youtu.be/oBXChy_Om48

#### Description:

Expense Manager is a personal finance web application built as my CS50 Final Project. The goal of the project is to provide users with a simple way to manage their finances by tracking income, expenses, and budgets from a single dashboard. Rather than recreating the CS50 Finance project, I wanted to build an application that solves a real-world problem and could continue to be expanded after the course.

The application is built using Flask as the backend framework, SQLite as the database, Jinja for server-side templating, and Bootstrap for the user interface. User authentication is implemented using Flask sessions, allowing each user to securely manage their own financial information. Every query that modifies or retrieves sensitive data verifies ownership through the authenticated user's session.

The dashboard serves as the main entry point of the application. It displays summary cards showing the user's current balance, total income, and total expenses. These values are calculated using SQL aggregation rather than Python loops, making the application more efficient and reinforcing the use of relational database operations. The dashboard also displays recent transactions and a budget overview, where Bootstrap progress bars visually represent how much of each budget has been spent.

Users can create, edit, and delete transactions through a full CRUD interface. Each transaction belongs to a category and stores a description, amount, and transaction date. Categories are divided into income and expense types, allowing the application to distinguish between money earned and money spent while producing accurate financial summaries.

The budgeting module allows users to create spending limits for expense categories. Instead of requiring users to recreate budgets every month, budgets remain active until they are edited or deleted. The application calculates the amount spent in each category, the remaining budget, and the percentage of the budget that has been used. These calculations are presented both as numerical values and as visual progress bars on the dashboard and the budgets page.

Throughout development I focused on reducing duplicated code by separating business logic from route handlers. Budget calculations were refactored into a reusable helper function that performs the necessary SQL queries, aggregates spending data, builds efficient dictionary lookups, and returns a single view-model that can be reused by multiple pages. This approach keeps route functions concise while making the application easier to maintain.

The database design consists of users, categories, transactions, and budgets. Relationships between these tables are implemented using foreign keys, and SQL JOIN operations are used extensively throughout the application. Aggregate queries using SUM(), GROUP BY, ORDER BY, and LIMIT are used to calculate balances, generate dashboard summaries, and retrieve recent transactions efficiently.

One design decision was to perform calculations in SQL whenever possible instead of retrieving all records and processing them in Python. This reduces unnecessary work in the application layer and demonstrates the strengths of relational databases. Another important design decision was constructing view-model dictionaries in Python before passing data to Jinja templates. This keeps presentation logic simple and prevents templates from becoming overly complex.

<<<<<<< HEAD
This project significantly improved my understanding of Flask application structure, SQL query design, database relationships, reusable helper functions, server-side rendering with Jinja, and building maintainable web applications. Although the project satisfies the requirements of the CS50 Final Project, I intend to continue developing it by migrating the database to PostgreSQL, adding financial reports and charts, supporting CSV bank statement imports, implementing automatic transaction categorization, and eventually building a native Swift iOS client that communicates with the same backend.
=======
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
- User authentication
- Session management
- Dashboard
- Transactions CRUD
- Categories management
- Budgets CRUD
- SQL aggregation and reporting
- Custom Jinja filters
- Reusable helper functions
- Responsive navigation
- Flash messaging
- Bootstrap-based user interface

Currently working on:

- Final testing and documentation
- CS50 project submission

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
>>>>>>> 85ecf34221e1cb9725ca9ce8c4117894baf61913
