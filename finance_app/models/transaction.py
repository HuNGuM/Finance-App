from dataclasses import dataclass
from typing import Optional

@dataclass
class Transaction:
    id: Optional[int]
    date: str
    amount: float
    category: str
    description: str
    type: str
    account_id: int

