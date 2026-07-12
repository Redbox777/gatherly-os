from core import Database, get_logger
from models import Meeting

logger = get_logger(__name__)

class MeetingRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(self, meeting: Meeting) -> int:
        """Создать встречу"""
        query = """
            INSERT INTO meetings (creator_id, title, description, date, time, place, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """
        cursor = self.db.execute(query, (
            meeting.creator_id,
            meeting.title,
            meeting.description,
            meeting.date,
            meeting.time,
            meeting.place,
            meeting.status
        ))
        return cursor.lastrowid

    def get_by_id(self, meeting_id: int) -> Meeting | None:
        query = "SELECT * FROM meetings WHERE id = ?"
        row = self.db.fetch_one(query, (meeting_id,))
        return Meeting.from_db(row) if row else None

    def get_by_user(self, user_id: int) -> list[Meeting]:
        """Получить все встречи пользователя (где он создатель или участник)"""
        query = """
            SELECT m.* FROM meetings m
            LEFT JOIN meeting_participants mp ON m.id = mp.meeting_id
            WHERE m.creator_id = ? OR mp.user_id = ?
            GROUP BY m.id
            ORDER BY m.date, m.time
        """
        rows = self.db.fetch_all(query, (user_id, user_id))
        return [Meeting.from_db(row) for row in rows]

    def update(self, meeting: Meeting) -> None:
        query = """
            UPDATE meetings
            SET title = ?, description = ?, date = ?, time = ?, place = ?, status = ?
            WHERE id = ?
        """
        self.db.execute(query, (
            meeting.title,
            meeting.description,
            meeting.date,
            meeting.time,
            meeting.place,
            meeting.status,
            meeting.id
        ))

    def delete(self, meeting_id: int) -> None:
        query = "DELETE FROM meetings WHERE id = ?"
        self.db.execute(query, (meeting_id,))
        # Удаляем участников
        self.db.execute("DELETE FROM meeting_participants WHERE meeting_id = ?", (meeting_id,))
