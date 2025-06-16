-- DROP TABLE IF EXISTS transactions;
-- DROP TABLE IF EXISTS categories;

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('income', 'expense'))
);
--
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
    account_id INTEGER,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
);
--
INSERT INTO categories (name, type) VALUES
('Food', 'expense'),
('Housing', 'expense'),
('Transport', 'expense'),
('Health', 'expense'),
('Cosmetics', 'expense'),
('Entertainment', 'expense'),
('Salary', 'income'),
('Scholarship', 'income'),
('Dividends', 'income');

    CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    balance REAL NOT NULL
);

-- ALTER TABLE transactions ADD COLUMN  account_id INTEGER REFERENCES accounts(id);