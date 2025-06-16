import sqlite3
import os
import sys

class Database:
    def __init__(self, db_file="finance.db"):
        self.conn = sqlite3.connect(db_file)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.create_schema()

    def create_schema(self):
        if hasattr(sys, '_MEIPASS'):
            # когда приложение запущено из .exe
            base_dir = os.path.join(sys._MEIPASS, 'db')
        else:
            # когда приложение запускается из исходников
            base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')

        migrations_path = os.path.join(base_dir, 'migrations.sql')

        with open(migrations_path, encoding="utf-8") as f:
            self.conn.executescript(f.read())
