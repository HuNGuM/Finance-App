from finance_app.models.transaction import Transaction

def test_transaction_creation():
    tx = Transaction(
        id=None,
        date="2025-06-01",
        amount=100.0,
        category="Food",
        description="Lunch",
        type="expense",
        account_id=1
    )
    assert tx.amount == 100.0
    assert tx.type == "expense"
