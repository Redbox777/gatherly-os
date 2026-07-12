from core import Database
from models import Poll

class PollRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(self, poll: Poll) -> int:
        query = """
            INSERT INTO polls (meeting_id, creator_id, question, options, created_at)
            VALUES (?, ?, ?, ?, datetime('now'))
        """
        cursor = self.db.execute(query, (poll.meeting_id, poll.creator_id, poll.question, poll.options))
        return cursor.lastrowid

    def get_by_meeting(self, meeting_id: int) -> list:
        query = "SELECT * FROM polls WHERE meeting_id = ? ORDER BY created_at DESC"
        rows = self.db.fetch_all(query, (meeting_id,))
        return [Poll.from_db(row) for row in rows]

    def get_by_id(self, poll_id: int):
        query = "SELECT * FROM polls WHERE id = ?"
        row = self.db.fetch_one(query, (poll_id,))
        return Poll.from_db(row) if row else None
