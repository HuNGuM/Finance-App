import pdfplumber
import re
from finance_app.models.transaction import Transaction
from datetime import datetime


def parse_pko_pdf(filepath: str) -> list[Transaction]:
    transactions = []

    pattern = re.compile(
        r"(\d{2}\.\d{2}\.\d{4})\s+\S+\s+([A-ZĄĆĘŁŃÓŚŹŻ\s\.\-]+?)\s+([−-]?\d{1,3}(?:\s?\d{3})*,\d{2})\s+[\d\s,]+"
    )

    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            for line in text.split("\n"):
                line = line.strip()
                match = pattern.match(line)

                if match:
                    op_date, op_type, amount_raw = match.groups()

                    amount = float(amount_raw.replace(" ", "").replace(",", ".").replace("−", "-"))
                    tx_type = "income" if amount > 0 else "expense"

                    transactions.append(Transaction(
                        id=None,
                        date=datetime.strptime(op_date, "%d.%m.%Y").strftime("%Y-%m-%d"),
                        amount=abs(amount),
                        category=tx_type,
                        description=op_type.strip().title(),
                        type=tx_type,
                        account_id=None
                    ))

    return transactions
