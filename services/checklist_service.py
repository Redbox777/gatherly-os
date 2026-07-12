from core import Database, get_logger
from repositories import ChecklistRepository
from models import Checklist

logger = get_logger(__name__)

class ChecklistService:
    def __init__(self, db: Database):
        self.db = db
        self.repo = ChecklistRepository(db)

    def add_task(self, meeting_id: int, user_id: int, task: str) -> int:
        item = Checklist(meeting_id=meeting_id, user_id=user_id, task=task)
        return self.repo.create(item)

    def get_tasks(self, meeting_id: int) -> list:
        return self.repo.get_by_meeting(meeting_id)

    def toggle_done(self, task_id: int, user_id: int) -> bool:
        return self.repo.toggle_done(task_id, user_id)

    def delete_task(self, task_id: int, user_id: int) -> bool:
        return self.repo.delete(task_id, user_id)
