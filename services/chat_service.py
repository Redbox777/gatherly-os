from core import Database, get_logger
from repositories import ChatRepository, MeetingRepository, ParticipantRepository
from models import Chat

logger = get_logger(__name__)

class ChatService:
    def __init__(self, db: Database):
        self.db = db
        self.chat_repo = ChatRepository(db)
        self.meeting_repo = MeetingRepository(db)
        self.participant_repo = ParticipantRepository(db)

    def send_message(self, meeting_id: int, user_id: int, message: str) -> bool:
        """Отправить сообщение в чат встречи"""
        meeting = self.meeting_repo.get_by_id(meeting_id)
        if not meeting:
            return False
        
        # Проверяем, является ли пользователь участником
        participants = self.participant_repo.get_by_meeting(meeting_id)
        if user_id not in [p.user_id for p in participants]:
            return False
        
        chat = Chat(meeting_id=meeting_id, user_id=user_id, message=message)
        self.chat_repo.save(chat)
        return True

    def get_chat(self, meeting_id: int) -> list:
        """Получить все сообщения чата встречи"""
        return self.chat_repo.get_by_meeting(meeting_id)
