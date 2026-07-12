from dataclasses import dataclass
from typing import Optional

@dataclass
class Chat:
    id: Optional[int] = None
    meeting_id: int = 0
    user_id: int = 0
    message: str = ""
    created_at: Optional[str] = None

    @classmethod
    def from_db(cls, row: dict) -> "Chat":
        return cls(
            id=row["id"],
            meeting_id=row["meeting_id"],
            user_id=row["user_id"],
            message=row["message"],
            created_at=row.get("created_at")
        )
