from finance_app.repositories.transaction_repo import TransactionRepository

class ReportService:
    def __init__(self, repo: TransactionRepository):
        self.repo = repo

    def get_total_by_category(self):
        cur = self.repo.conn.cursor()
        cur.execute("SELECT category, SUM(amount) FROM transactions GROUP BY category")
        return cur.fetchall()
