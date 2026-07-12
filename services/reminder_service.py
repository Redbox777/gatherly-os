from core import Database, get_logger
from repositories import ReminderRepository
from models import Reminder
from datetime import datetime

logger = get_logger(__name__)

class ReminderService:
    def __init__(self, db: Database):
        self.db = db
        self.repo = ReminderRepository(db)

    def schedule(self, user_id: int, chat_id: int, text: str, remind_at: str) -> int:
        """Создать напоминание"""
        try:
            # Проверяем формат даты
            datetime.fromisoformat(remind_at)
        except ValueError:
            return -1
        
        reminder = Reminder(
            user_id=user_id,
            chat_id=chat_id,
            text=text,
            remind_at=remind_at
        )
        reminder_id = self.repo.create(reminder)
        logger.info(f"Напоминание #{reminder_id} для {user_id}: {text} в {remind_at}")
        return reminder_id

    def get_pending(self) -> list[Reminder]:
        """Получить все ожидающие напоминания"""
        return self.repo.get_pending()

    def get_user_reminders(self, user_id: int) -> list[Reminder]:
        """Получить все напоминания пользователя"""
        return self.repo.get_by_user(user_id)

    def delete(self, user_id: int, reminder_id: int) -> bool:
        """Удалить напоминание"""
        return self.repo.delete_by_user(user_id, reminder_id)

    def check_and_send(self, send_callback) -> None:
        """Проверить и отправить все напоминания"""
        reminders = self.get_pending()
        for r in reminders:
            send_callback(r.chat_id, f"⏰ Напоминание: {r.text}")
            self.repo.delete(r.id)
            logger.info(f"Напоминание #{r.id} отправлено")
