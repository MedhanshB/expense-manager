# Product Requirements Document (PRD)

# Expense Manager

Version: 0.1
Status: Draft
Author: <Med>

---

# 1. Purpose

A brief paragraph explaining why this application exists.
This app is being created for personal use over using the current apps instead they also solve similar problems but this is for personal use. Existing apps solve similar problems, but this is being built for personal use and to be portfolio-worthy, not because no alternative exists.
---

# 2. Problem Statement

Describe the user's problem without mentioning implementation.
The user experiences going through their payments and not knowing where the money was used, it is very hectic to try and remember or narrow down where this transaction was done and what it actually is. This app is being created for personal use over using the current apps instead they also solve similar problems but this is for personal use

---

# 3. Target User

Primary User is probably someone who does not have time to note down every transaction, and getting them into a habit of recording their transactions. This app helps with quick manual entry at the time of purchase, whether you paid using cash or any banking facility. 
Typical usage would be done daily to maybe weekly or monthly depending on how the user wants to.

---

# 4. Project Goals

List the goals of Version 1.
Finish the basic foundation of the app through being able to create an account, log in and then enter the transactions into categories.
This tracks expenses and income, puts the money spent into desired categories, then compare how you spent your money. Also help view the financial summary.

---

# 5. Functional Requirements

## Authentication

The application shall:

- Register users
- Log users in
- Log users out


---

## Transactions

The application shall:

- Create transactions
- Edit transactions
- Delete transactions
- View transaction history
- Let users enter expenses into categories
- Every transaction requires a description. If the selected category is Other, the description should clearly explain the purchase since the category itself provides no useful context.

Every transaction must include:

- Amount
- Category
- Description
- Date (Automatically taken)
- Type (Income / Expense)

---

## Categories

The application shall:

- Provide predefined categories
- Include an "Others" category
- Prevent users from modifying categories

---

## Budgets

The application shall:

- Allow one monthly budget per category
- Compare spending against the current month's budget

---

## Dashboard

The application shall display:

- Current month's income
- Current month's expenses
- Remaining balance
- Spending by category
- Budget progress
- Recent transactions

---

# 6. Business Rules

Rules that define how the application behaves.

- Amounts are stored as integer paise.
- Every transaction belongs to exactly one category.
- Every transaction requires a description.
- Categories are predefined.
- Budget periods are calendar months.
- Foreign keys must be enforced.

---

# 7. Non-Functional Requirements

The application should:

- Use Flask
- Use SQLite
- Use server-side rendering
- Provide secure authentication
- Be responsive
- Validate all user input
- Store financial data accurately

---

# 8. Out of Scope

Explicitly excluded from Version 1.

- CSV import
- Bank synchronization
- Mobile application
- Notifications
- AI categorization
- Receipt scanning
- Multiple accounts

---

# 9. Assumptions

- Users manually enter transactions. Until the CSV import feature in the next run.
- Categories remain fixed.
- Budgets reset every calendar month.

---

# 10. Success Criteria

Version 1 is complete when a user can:

- Register
- Log in
- Add income
- Add expenses
- View spending history
- Set budgets
- Compare budgets against spending
- Log out

---

# 11. Future Enhancements

Reference BACKLOG.md.

- CSV imports
- Merchant recognition
- Recurring transactions
- Better analytics