from core import Database
from models import Chat

class ChatRepository:
    def __init__(self, db: Database):
        self.db = db

    def save(self, chat: Chat) -> int:
        query = """
            INSERT INTO chats (meeting_id, user_id, message, created_at)
            VALUES (?, ?, ?, datetime('now'))
        """
        cursor = self.db.execute(query, (chat.meeting_id, chat.user_id, chat.message))
        return cursor.lastrowid

    def get_by_meeting(self, meeting_id: int) -> list:
        query = "SELECT * FROM chats WHERE meeting_id = ? ORDER BY created_at"
        rows = self.db.fetch_all(query, (meeting_id,))
        return [Chat.from_db(row) for row in rows]
