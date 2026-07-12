from dataclasses import dataclass
from typing import Optional

@dataclass
class Reminder:
    id: Optional[int] = None
    user_id: int = 0
    chat_id: int = 0
    text: str = ""
    remind_at: str = ""  # ISO формат: 2026-07-12T18:00:00
    created_at: Optional[str] = None

    @classmethod
    def from_db(cls, row: dict) -> "Reminder":
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            chat_id=row["chat_id"],
            text=row["text"],
            remind_at=row["remind_at"],
            created_at=row.get("created_at")
        )
