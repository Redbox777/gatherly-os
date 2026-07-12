from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    user_id: int
    first_name: str
    username: Optional[str] = None
    city: Optional[str] = None
    timezone: Optional[str] = None
    interests: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_db(cls, row: dict) -> "User":
        return cls(
            user_id=row["user_id"],
            first_name=row["first_name"],
            username=row.get("username"),
            city=row.get("city"),
            timezone=row.get("timezone"),
            interests=row.get("interests"),
            created_at=row.get("created_at")
        )
