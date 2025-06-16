from finance_app.models.transaction import Transaction


def test_transaction_model():
    tx = Transaction(
        id=None,
        date="2025-06-15",
        amount=100.0,
        category="Food",
        description="Groceries",
        type="expense",
        account_id=1
    )

    assert tx.amount == 100.0
    assert tx.type == "expense"
    assert tx.account_id == 1
