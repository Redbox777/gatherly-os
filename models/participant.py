from dataclasses import dataclass

@dataclass
class Participant:
    meeting_id: int
    user_id: int
    status: str  # going, not_going, maybe

    @classmethod
    def from_db(cls, row: dict) -> "Participant":
        return cls(
            meeting_id=row["meeting_id"],
            user_id=row["user_id"],
            status=row["status"]
        )
