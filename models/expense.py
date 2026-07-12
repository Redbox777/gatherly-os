from dataclasses import dataclass
from typing import Optional

@dataclass
class Expense:
    id: int
    meeting_id: int
    user_id: int
    amount: float
    description: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_db(cls, row: dict) -> "Expense":
        return cls(
            id=row["id"],
            meeting_id=row["meeting_id"],
            user_id=row["user_id"],
            amount=row["amount"],
            description=row.get("description"),
            created_at=row.get("created_at")
        )
