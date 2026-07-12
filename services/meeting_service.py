from datetime import datetime
from core import Database, get_logger
from repositories import MeetingRepository, ParticipantRepository
from models import Meeting, Participant

logger = get_logger(__name__)

class MeetingService:
    def __init__(self, db: Database):
        self.db = db
        self.meeting_repo = MeetingRepository(db)
        self.participant_repo = ParticipantRepository(db)

    def create_meeting(self, creator_id: int, title: str, description: str = None,
                       date: str = None, time: str = None, place: str = None) -> int:
        """Создать новую встречу"""
        meeting = Meeting(
            creator_id=creator_id,
            title=title,
            description=description,
            date=date,
            time=time,
            place=place,
            status="active"
        )
        meeting_id = self.meeting_repo.create(meeting)
        
        # Создатель автоматически становится участником со статусом "going"
        self.participant_repo.save(Participant(
            meeting_id=meeting_id,
            user_id=creator_id,
            status="going"
        ))
        
        logger.info(f"Создана встреча #{meeting_id}: {title}")
        return meeting_id

    def get_meeting(self, meeting_id: int) -> dict:
        """Получить информацию о встрече с участниками"""
        meeting = self.meeting_repo.get_by_id(meeting_id)
        if not meeting:
            return {"error": "Встреча не найдена"}
        
        participants = self.participant_repo.get_by_meeting(meeting_id)
        
        going = [p.user_id for p in participants if p.status == "going"]
        not_going = [p.user_id for p in participants if p.status == "not_going"]
        maybe = [p.user_id for p in participants if p.status == "maybe"]
        
        return {
            "id": meeting.id,
            "title": meeting.title,
            "description": meeting.description or "—",
            "date": meeting.date or "Не указана",
            "time": meeting.time or "Не указано",
            "place": meeting.place or "Не указано",
            "creator_id": meeting.creator_id,
            "status": meeting.status,
            "going": going,
            "not_going": not_going,
            "maybe": maybe,
            "created_at": meeting.created_at
        }

    def get_user_meetings(self, user_id: int) -> list:
        """Получить все встречи пользователя"""
        meetings = self.meeting_repo.get_by_user(user_id)
        result = []
        for m in meetings:
            participants = self.participant_repo.get_by_meeting(m.id)
            going = len([p for p in participants if p.status == "going"])
            not_going = len([p for p in participants if p.status == "not_going"])
            maybe = len([p for p in participants if p.status == "maybe"])
            
            result.append({
                "id": m.id,
                "title": m.title,
                "date": m.date or "?",
                "time": m.time or "?",
                "place": m.place or "?",
                "going": going,
                "not_going": not_going,
                "maybe": maybe
            })
        return result

    def vote(self, meeting_id: int, user_id: int, status: str) -> bool:
        """Голосование за встречу (going, not_going, maybe)"""
        if status not in ["going", "not_going", "maybe"]:
            return False
        
        meeting = self.meeting_repo.get_by_id(meeting_id)
        if not meeting:
            return False
        
        self.participant_repo.save(Participant(
            meeting_id=meeting_id,
            user_id=user_id,
            status=status
        ))
        return True

    def delete_meeting(self, meeting_id: int, user_id: int) -> bool:
        """Удалить встречу (только создатель)"""
        meeting = self.meeting_repo.get_by_id(meeting_id)
        if not meeting or meeting.creator_id != user_id:
            return False
        
        self.meeting_repo.delete(meeting_id)
        logger.info(f"Встреча #{meeting_id} удалена")
        return True
