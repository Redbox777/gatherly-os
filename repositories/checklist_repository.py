from core import Database
from models import Checklist

class ChecklistRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(self, item: Checklist) -> int:
        query = """
            INSERT INTO checklists (meeting_id, user_id, task, done, created_at)
            VALUES (?, ?, ?, ?, datetime('now'))
        """
        cursor = self.db.execute(query, (item.meeting_id, item.user_id, item.task, 0))
        return cursor.lastrowid

    def get_by_meeting(self, meeting_id: int) -> list:
        query = "SELECT * FROM checklists WHERE meeting_id = ? ORDER BY created_at"
        rows = self.db.fetch_all(query, (meeting_id,))
        return [Checklist.from_db(row) for row in rows]

    def toggle_done(self, item_id: int, user_id: int) -> bool:
        query = "UPDATE checklists SET done = 1 - done WHERE id = ? AND user_id = ?"
        cursor = self.db.execute(query, (item_id, user_id))
        return cursor.rowcount > 0

    def delete(self, item_id: int, user_id: int) -> bool:
        query = "DELETE FROM checklists WHERE id = ? AND user_id = ?"
        cursor = self.db.execute(query, (item_id, user_id))
        return cursor.rowcount > 0
