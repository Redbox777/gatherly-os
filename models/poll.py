from dataclasses import dataclass
from typing import Optional

@dataclass
class Poll:
    id: Optional[int] = None
    meeting_id: int = 0
    creator_id: int = 0
    question: str = ""
    options: str = ""  # JSON список
    created_at: Optional[str] = None

    @classmethod
    def from_db(cls, row: dict) -> "Poll":
        return cls(
            id=row["id"],
            meeting_id=row["meeting_id"],
            creator_id=row["creator_id"],
            question=row["question"],
            options=row["options"],
            created_at=row.get("created_at")
        )
