from finance_app.models.transaction import Transaction
from finance_app.db.database import Database
from typing import List
import datetime

class TransactionRepository:
    def __init__(self, db: Database):
        self.conn = db.conn

    def add(self, transaction: Transaction):
        with self.conn:
            self.conn.execute("""
                INSERT INTO transactions (date, amount, category, description, type, account_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                transaction.date,
                transaction.amount,
                transaction.category,
                transaction.description,
                transaction.type,
                transaction.account_id
            ))


    def get_all(self) -> List[Transaction]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM transactions ORDER BY date DESC")
        rows = cur.fetchall()
        return [Transaction(*row) for row in rows]

    def get_by_type_and_period(self, tx_type, start_date, end_date, category=None, account_id=None):
        query = "SELECT id, date, amount, category, description, type, account_id FROM transactions WHERE type = ? AND date BETWEEN ? AND ?"
        params = [tx_type, start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        if account_id:
            query += " AND account_id = ?"
            params.append(account_id)

        cur = self.conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        return [Transaction(*row) for row in rows]

    def delete_transaction(self, date: str, amount: float, category: str, description: str):
        with self.conn:
            self.conn.execute(
                "DELETE FROM transactions WHERE rowid = (SELECT rowid FROM transactions WHERE date = ? AND amount = ? AND category = ? AND description = ? LIMIT 1)",
                (date, amount, category, description)
            )

    def update_transaction(self, old_date, old_amount, old_category, old_description, new_tx: Transaction):
        with self.conn:
            self.conn.execute("""
                UPDATE transactions SET date = ?, amount = ?, category = ?, description = ?
                WHERE date = ? AND amount = ? AND category = ? AND description = ?
            """, (
                new_tx.date, new_tx.amount, new_tx.category, new_tx.description,
                old_date, old_amount, old_category, old_description
            ))
