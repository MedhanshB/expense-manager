CREATE TABLE users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE categories (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('Expense', 'Income')),
    UNIQUE (name, type)
);

CREATE TABLE transactions (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    amount INTEGER NOT NULL CHECK (amount > 0),
    description TEXT NOT NULL,
    transaction_date DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);


CREATE TABLE budgets (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    budget_amount INTEGER NOT NULL,
    budget_period TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    UNIQUE (user_id, category_id, budget_period)
);

INSERT INTO categories (name, type) VALUES
('Food & Dining', 'Expense'),
('Transport', 'Expense'),
('Housing', 'Expense'),
('Utilities', 'Expense'),
('Shopping', 'Expense'),
('Health', 'Expense'),
('Education', 'Expense'),
('Entertainment', 'Expense'),
('Subscriptions', 'Expense'),
('Travel', 'Expense'),
('Other', 'Expense'),

('Salary', 'Income'),
('Freelance', 'Income'),
('Investment', 'Income'),
('Gift', 'Income'),
('Refund', 'Income'),
('Other Income', 'Income');