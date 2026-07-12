from bot_core.client import TelegramClient
from services import ReminderService
from core import Database
from bot_core.keyboards import main_menu, back_menu
from datetime import datetime

class ReminderHandler:
    def __init__(self, client: TelegramClient, db: Database):
        self.client = client
        self.reminder_service = ReminderService(db)

    def schedule(self, chat_id: int, text: str):
        """Обработчик создания напоминания /remind"""
        parts = text.split(maxsplit=2)
        if len(parts) < 3:
            self.client.send_message(
                chat_id,
                "❌ Формат: /remind 2026-07-12T18:00 Описание",
                main_menu()
            )
            return
        
        try:
            remind_at = parts[1]
            reminder_text = parts[2]
            reminder_id = self.reminder_service.schedule(
                user_id=chat_id,
                chat_id=chat_id,
                text=reminder_text,
                remind_at=remind_at
            )
            if reminder_id > 0:
                self.client.send_message(
                    chat_id,
                    f"✅ Напоминание создано!\n🕐 {remind_at}\n📝 {reminder_text}",
                    main_menu()
                )
            else:
                self.client.send_message(
                    chat_id,
                    "❌ Ошибка: неверный формат даты. Используйте YYYY-MM-DDTHH:MM",
                    main_menu()
                )
        except Exception as e:
            self.client.send_message(
                chat_id,
                f"❌ Ошибка: {e}",
                main_menu()
            )

    def list_reminders(self, chat_id: int):
        """Показать все напоминания"""
        reminders = self.reminder_service.get_user_reminders(chat_id)
        if not reminders:
            self.client.send_message(
                chat_id,
                "📭 У вас пока нет напоминаний.",
                main_menu()
            )
            return
        
        text = "⏰ **Ваши напоминания:**\n\n"
        for r in reminders:
            text += f"#{r.id} {r.remind_at} — {r.text}\n"
        
        self.client.send_message(
            chat_id,
            text,
            main_menu()
        )

    def delete(self, chat_id: int, reminder_id_str: str):
        """Удалить напоминание"""
        try:
            reminder_id = int(reminder_id_str)
        except ValueError:
            self.client.send_message(
                chat_id,
                "❌ Введите корректный ID напоминания.",
                main_menu()
            )
            return
        
        if self.reminder_service.delete(chat_id, reminder_id):
            self.client.send_message(
                chat_id,
                f"✅ Напоминание #{reminder_id} удалено.",
                main_menu()
            )
        else:
            self.client.send_message(
                chat_id,
                f"❌ Напоминание #{reminder_id} не найдено.",
                main_menu()
            )
