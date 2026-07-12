import json
from core import Database, get_logger
from repositories import PollRepository, MeetingRepository, ParticipantRepository
from models import Poll

logger = get_logger(__name__)

class PollService:
    def __init__(self, db: Database):
        self.db = db
        self.poll_repo = PollRepository(db)
        self.meeting_repo = MeetingRepository(db)
        self.participant_repo = ParticipantRepository(db)

    def create_poll(self, meeting_id: int, creator_id: int, question: str, options: list) -> int:
        """Создать опрос"""
        meeting = self.meeting_repo.get_by_id(meeting_id)
        if not meeting:
            return -1
        
        poll = Poll(
            meeting_id=meeting_id,
            creator_id=creator_id,
            question=question,
            options=json.dumps(options)
        )
        return self.poll_repo.create(poll)

    def get_polls(self, meeting_id: int) -> list:
        """Получить все опросы встречи"""
        return self.poll_repo.get_by_meeting(meeting_id)

    def vote(self, poll_id: int, user_id: int, option_index: int) -> bool:
        """Проголосовать в опросе"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT OR REPLACE INTO poll_votes (poll_id, user_id, option_index) VALUES (?, ?, ?)",
                (poll_id, user_id, option_index)
            )
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Ошибка голосования: {e}")
            return False
        finally:
            conn.close()
