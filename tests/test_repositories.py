import pytest

from finance_app.db.database import Database
from finance_app.repositories.account_repo import AccountRepository

@pytest.fixture
def in_memory_repo():
    db = Database(":memory:")
    db.conn.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, balance REAL)")
    return AccountRepository(db)

def test_add_and_get_account(in_memory_repo):
    in_memory_repo.add_account("TestAccount", 500.0)
    accounts = in_memory_repo.get_all()
    assert len(accounts) == 1
    assert accounts[0].name == "TestAccount"
    assert accounts[0].balance == 500.0
