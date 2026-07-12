from core import Database
from models import Participant

class ParticipantRepository:
    def __init__(self, db: Database):
        self.db = db

    def save(self, participant: Participant) -> None:
        """Сохранить статус участника"""
        query = """
            INSERT OR REPLACE INTO meeting_participants (meeting_id, user_id, status)
            VALUES (?, ?, ?)
        """
        self.db.execute(query, (
            participant.meeting_id,
            participant.user_id,
            participant.status
        ))

    def get_by_meeting(self, meeting_id: int) -> list[Participant]:
        query = "SELECT * FROM meeting_participants WHERE meeting_id = ?"
        rows = self.db.fetch_all(query, (meeting_id,))
        return [Participant.from_db(row) for row in rows]

    def get_by_user(self, user_id: int) -> list[Participant]:
        query = "SELECT * FROM meeting_participants WHERE user_id = ?"
        rows = self.db.fetch_all(query, (user_id,))
        return [Participant.from_db(row) for row in rows]

    def delete(self, meeting_id: int, user_id: int) -> None:
        query = "DELETE FROM meeting_participants WHERE meeting_id = ? AND user_id = ?"
        self.db.execute(query, (meeting_id, user_id))
