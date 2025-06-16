from finance_app.db.database import Database
from finance_app.repositories.transaction_repo import TransactionRepository
from finance_app.ui.main_window import MainWindow
import tkinter as tk

if __name__ == "__main__":
    db = Database()
    repo = TransactionRepository(db)

    root = tk.Tk()
    app = MainWindow(root, repo, db)
    root.mainloop()
