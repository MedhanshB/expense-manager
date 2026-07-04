# UI Wireframes

## Dashboard

Purpose: Give the user an immediate overview of their financial health.
This page is read-only and acts as a summary.

``` text
-----------------------------------------------------
 Navbar
-----------------------------------------------------

Hello, <User> 👋

-----------------------------------------------------
 Remaining Balance
 ₹18,450
-----------------------------------------------------

+----------------+----------------+----------------+
| Income         | Expenses       | Savings        |
| ₹45,000        | ₹26,550        | ₹18,450        |
+----------------+----------------+----------------+

-----------------------------------------------------
 Spending by Category (Pie Chart)
-----------------------------------------------------

-----------------------------------------------------
 Budget Progress (Progress Bars)
-----------------------------------------------------

-----------------------------------------------------
 Recent Transactions (Last 5)
-----------------------------------------------------

Date        Category      Description      Amount
-------------------------------------------------
05 Jul      Food          Lunch            ₹350
04 Jul      Salary        July Salary      ₹45,000
03 Jul      Transport     Metro Card       ₹200

[View All Transactions]
```

### Dashboard Components

-   Navbar
-   Remaining Balance card
-   Income card
-   Expenses card
-   Savings/Net Balance card
-   Spending by Category chart
-   Budget Progress section
-   Recent Transactions table

------------------------------------------------------------------------

## Transactions

Purpose: Manage all income and expense records.

``` text
-----------------------------------------------------
 Navbar
-----------------------------------------------------

Transactions

Filters:
[Month] [Category] [Type] [Search]

                    [+ Add Transaction]

-----------------------------------------------------

Date | Category | Description | Amount | Edit | Delete

-----------------------------------------------------

05 Jul | Food | Lunch | ₹350 | ✏ | 🗑
04 Jul | Salary | July Salary | ₹45,000 | ✏ | 🗑
03 Jul | Transport | Metro Card | ₹200 | ✏ | 🗑

-----------------------------------------------------

< Previous                Next >
```

### Transactions Components

-   Filter controls
-   Search bar
-   Add Transaction button
-   Transactions table
-   Edit/Delete actions
-   Pagination (optional for MVP)
