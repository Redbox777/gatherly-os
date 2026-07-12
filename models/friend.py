from dataclasses import dataclass
from typing import Optional

@dataclass
class Friend:
    user_id: int
    friend_id: int
    status: str  # pending, accepted, rejected
    created_at: Optional[str] = None

    @classmethod
    def from_db(cls, row: dict) -> "Friend":
        return cls(
            user_id=row["user_id"],
            friend_id=row["friend_id"],
            status=row["status"],
            created_at=row.get("created_at")
        )
