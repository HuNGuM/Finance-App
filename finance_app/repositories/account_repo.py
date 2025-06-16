from finance_app.models.account import Account
from finance_app.db.database import Database
from typing import List, Optional

class AccountRepository:
    def __init__(self, db: Database):
        self.conn = db.conn

    def get_all(self) -> List[Account]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, balance FROM accounts ORDER BY name")
        rows = cur.fetchall()
        return [Account(*row) for row in rows]

    def get_by_id(self, account_id: int) -> Optional[Account]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, balance FROM accounts WHERE id = ?", (account_id,))
        row = cur.fetchone()
        return Account(*row) if row else None

    def add_account(self, name: str, balance: float) -> None:
        with self.conn:
            self.conn.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, balance))

    def update_account(self, account_id: int, new_name: str, new_balance: float) -> None:
        with self.conn:
            self.conn.execute(
                "UPDATE accounts SET name = ?, balance = ? WHERE id = ?",
                (new_name, new_balance, account_id)
            )

    def delete_account(self, account_id: int) -> None:
        with self.conn:
            self.conn.execute("DELETE FROM accounts WHERE id = ?", (account_id,))

    def get_by_name(self, name: str) -> Optional[Account]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, balance FROM accounts WHERE name = ?", (name,))
        row = cur.fetchone()
        return Account(*row) if row else None
