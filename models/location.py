from dataclasses import dataclass
from typing import Optional

@dataclass
class Location:
    id: Optional[int] = None
    user_id: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    place_name: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_db(cls, row: dict) -> "Location":
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            latitude=row["latitude"],
            longitude=row["longitude"],
            place_name=row.get("place_name"),
            created_at=row.get("created_at")
        )
