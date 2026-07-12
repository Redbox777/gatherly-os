from core import Database
from models import Reminder
from datetime import datetime

class ReminderRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(self, reminder: Reminder) -> int:
        query = """
            INSERT INTO reminders (user_id, chat_id, text, remind_at, created_at)
            VALUES (?, ?, ?, ?, datetime('now'))
        """
        cursor = self.db.execute(query, (
            reminder.user_id,
            reminder.chat_id,
            reminder.text,
            reminder.remind_at
        ))
        return cursor.lastrowid

    def get_pending(self) -> list:
        now = datetime.now().isoformat()
        query = "SELECT * FROM reminders WHERE remind_at <= ?"
        rows = self.db.fetch_all(query, (now,))
        return [Reminder.from_db(row) for row in rows]

    def delete(self, reminder_id: int) -> None:
        query = "DELETE FROM reminders WHERE id = ?"
        self.db.execute(query, (reminder_id,))

    def get_by_user(self, user_id: int) -> list:
        query = "SELECT * FROM reminders WHERE user_id = ? ORDER BY remind_at"
        rows = self.db.fetch_all(query, (user_id,))
        return [Reminder.from_db(row) for row in rows]

    def delete_by_user(self, user_id: int, reminder_id: int) -> bool:
        query = "DELETE FROM reminders WHERE id = ? AND user_id = ?"
        cursor = self.db.execute(query, (reminder_id, user_id))
        return cursor.rowcount > 0
