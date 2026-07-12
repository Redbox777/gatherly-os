from dataclasses import dataclass
from typing import Optional

@dataclass
class Checklist:
    id: Optional[int] = None
    meeting_id: int = 0
    user_id: int = 0
    task: str = ""
    done: bool = False
    created_at: Optional[str] = None

    @classmethod
    def from_db(cls, row: dict) -> "Checklist":
        return cls(
            id=row["id"],
            meeting_id=row["meeting_id"],
            user_id=row["user_id"],
            task=row["task"],
            done=bool(row["done"]),
            created_at=row.get("created_at")
        )
