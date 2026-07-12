from dataclasses import dataclass
from typing import Optional

@dataclass
class Meeting:
    id: Optional[int] = None  # теперь id необязательный
    creator_id: int = 0
    title: str = ""
    description: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    place: Optional[str] = None
    status: str = "active"
    created_at: Optional[str] = None

    @classmethod
    def from_db(cls, row: dict) -> "Meeting":
        return cls(
            id=row["id"],
            creator_id=row["creator_id"],
            title=row["title"],
            description=row.get("description"),
            date=row.get("date"),
            time=row.get("time"),
            place=row.get("place"),
            status=row.get("status", "active"),
            created_at=row.get("created_at")
        )
