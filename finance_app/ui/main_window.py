import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from finance_app.repositories.category_repo import CategoryRepository
from finance_app.repositories.account_repo import AccountRepository
from finance_app.backend import backend

class MainWindow:

    def __init__(self, root, repo, db):
        for name in dir(backend):
            if callable(getattr(backend, name)) and not name.startswith("__"):
                setattr(MainWindow, name, getattr(backend, name))
        self.root = root
        self.repo = repo
        self.cat_repo = CategoryRepository(db)
        self.account_repo = AccountRepository(db)

        self.root.title("Finance Manager")

        self.current_type = "expense"
        self.date_filter = "month"

        self.setup_ui()
        self.load_accounts()
        self.load_categories()
        self.refresh_view()

        self.sort_column = None
        self.sort_reverse = False

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.expense_frame = ttk.Frame(self.notebook)
        self.income_frame = ttk.Frame(self.notebook)
        self.setup_accounts_tab()

        self.notebook.add(self.expense_frame, text="Expenses")
        self.notebook.add(self.income_frame, text="Income")
        self.notebook.pack(expand=True, fill="both")

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        self.total_label = ttk.Label(self.root, text="Amount: 0.00", font=("Arial", 12))
        self.total_label.pack(pady=5)

        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=5)

        for label, value in [("Day", "day"), ("Week", "week"), ("Month", "month")]:
            ttk.Button(filter_frame, text=label, command=lambda v=value: self.set_filter(v)).pack(side="left", padx=2)

        ttk.Label(filter_frame, text="From:").pack(side="left", padx=5)
        self.date_from = DateEntry(filter_frame, width=10)
        self.date_from.pack(side="left")
        ttk.Label(filter_frame, text="To:").pack(side="left")
        self.date_to = DateEntry(filter_frame, width=10)
        self.date_to.pack(side="left")
        ttk.Button(filter_frame, text="Show", command=lambda: self.set_filter("custom")).pack(side="left", padx=5)

        cat_frame = ttk.Frame(self.root)
        cat_frame.pack(pady=5)

        ttk.Label(cat_frame, text="Categories:").pack(side="left", padx=5)
        self.cat_var = tk.StringVar()
        self.cat_combo = ttk.Combobox(cat_frame, textvariable=self.cat_var, state="readonly", width=25)
        self.filter_by_cat_var = tk.BooleanVar(value=False)
        self.filter_by_cat_cb = ttk.Checkbutton(cat_frame, text="Filter by category",
        variable=self.filter_by_cat_var, command=self.refresh_view)
        self.filter_by_cat_cb.pack(side="left", padx=5)

        self.cat_combo.pack(side="left")
        ttk.Button(cat_frame, text="+ Add category", command=self.add_new_category).pack(side="left", padx=5)

        entry_frame = ttk.Frame(self.root)
        entry_frame.pack(pady=10)

        ttk.Label(cat_frame, text="Account:").pack(side="left", padx=5)
        self.filter_account_var = tk.StringVar()
        self.filter_account_combo = ttk.Combobox(cat_frame, textvariable=self.filter_account_var, state="readonly",
                                                 width=20)
        self.filter_account_combo.pack(side="left", padx=5)
        self.filter_account_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_view())

        ttk.Label(entry_frame, text="Account:").grid(row=0, column=6)
        self.account_var = tk.StringVar()
        self.account_combo = ttk.Combobox(entry_frame, textvariable=self.account_var, state="readonly", width=20)
        self.account_combo.grid(row=0, column=7, padx=5)

        ttk.Label(entry_frame, text="Amount:").grid(row=0, column=0)
        self.amount_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.amount_var, width=10).grid(row=0, column=1, padx=5)

        ttk.Label(entry_frame, text="Description:").grid(row=0, column=2)
        self.desc_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.desc_var, width=20).grid(row=0, column=3, padx=5)

        ttk.Label(entry_frame, text="Date:").grid(row=0, column=4)
        self.date_var = DateEntry(entry_frame, width=10)
        self.date_var.grid(row=0, column=5, padx=5)

        ttk.Button(entry_frame, text="Add transaction", command=self.add_transaction).grid(row=0, column=6, padx=10)


        self.table = ttk.Treeview(self.root, columns=("Date", "Amount", "Category", "Description", "Account"),
                                  show="headings")
        for col in self.table["columns"]:
            self.table.heading(col, text=col, command=lambda _col=col: self.sort_by_column(_col))
        self.table.pack(fill="both", expand=True, padx=10, pady=10)
        action_frame = ttk.Frame(self.root)
        action_frame.pack(pady=5)

        ttk.Button(action_frame, text="Edit", command=self.edit_transaction).pack(side="left", padx=10)
        ttk.Button(action_frame, text="Delete", command=self.delete_transaction).pack(side="left", padx=10)

        ttk.Button(self.root, text="Show report", command=self.show_report).pack(pady=10)
        ttk.Button(self.root, text="Import from PDF (PKO)", command=self.import_pdf).pack(pady=5)

        export_frame = ttk.Frame(self.root)
        export_frame.pack(pady=5)

        ttk.Button(export_frame, text="Export as CSV", command=self.export_as_csv).pack(side="left", padx=5)
        ttk.Button(export_frame, text="Export as PDF", command=self.export_as_pdf).pack(side="left", padx=5)
        ttk.Button(export_frame, text="Export as Excel", command=self.export_as_excel).pack(side="left", padx=5)

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

