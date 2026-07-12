from dataclasses import dataclass
from typing import Optional

@dataclass
class Folder:
    id: Optional[int] = None
    user_id: int = 0
    name: str = ""
    created_at: Optional[str] = None

    @classmethod
    def from_db(cls, row: dict) -> "Folder":
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            name=row["name"],
            created_at=row.get("created_at")
        )
