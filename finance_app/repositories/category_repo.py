from typing import List, Tuple
from finance_app.db.database import Database

class CategoryRepository:
    def __init__(self, db: Database):
        self.conn = db.conn

    def get_by_type(self, cat_type: str) -> List[str]:
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM categories WHERE type = ? ORDER BY name", (cat_type,))
        return [row[0] for row in cur.fetchall()]

    def add_category(self, name: str, cat_type: str):
        with self.conn:
            self.conn.execute("INSERT INTO categories (name, type) VALUES (?, ?)", (name, cat_type))
