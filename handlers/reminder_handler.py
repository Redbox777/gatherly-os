from bot_core.client import TelegramClient
from services import ReminderService
from core import Database
from bot_core.keyboards import main_menu, reminders_menu, back_menu
from datetime import datetime

class ReminderHandler:
    def __init__(self, client: TelegramClient, db: Database):
        self.client = client
        self.reminder_service = ReminderService(db)
        self.states = {}

    def show_menu(self, chat_id: int):
        self.client.send_message(
            chat_id,
            "⏰ **Меню напоминаний**\n\n"
            "➕ Создать — новое напоминание\n"
            "📋 Мои — список всех напоминаний\n"
            "❌ Удалить — удалить по ID",
            reminders_menu(),
            parse_mode="Markdown"
        )

    def start_create(self, chat_id: int):
        self.client.send_message(
            chat_id,
            "📝 Введите дату и время в формате:\n"
            "`2026-07-12T18:00`\n\n"
            "Затем через пробел напишите текст напоминания.\n"
            "Пример: `2026-07-12T18:00 Встреча с друзьями`",
            back_menu()
        )
        self.states[chat_id] = {"step": "waiting_remind"}

    def process_create(self, chat_id: int, text: str):
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            self.client.send_message(
                chat_id,
                "❌ Неверный формат.\n"
                "Пример: `2026-07-12T18:00 Встреча с друзьями`",
                reminders_menu()
            )
            return

        remind_at = parts[0]
        reminder_text = parts[1]

        try:
            datetime.fromisoformat(remind_at)
        except ValueError:
            self.client.send_message(
                chat_id,
                "❌ Неверный формат даты.\n"
                "Используйте: `YYYY-MM-DDTHH:MM`\n"
                "Пример: `2026-07-12T18:00`",
                reminders_menu()
            )
            return

        reminder_id = self.reminder_service.schedule(chat_id, chat_id, reminder_text, remind_at)
        if reminder_id > 0:
            self.client.send_message(
                chat_id,
                f"✅ Напоминание создано!\n\n"
                f"🕐 {remind_at}\n"
                f"📝 {reminder_text}\n"
                f"🆔 ID: {reminder_id}",
                reminders_menu()
            )
        else:
            self.client.send_message(
                chat_id,
                "❌ Ошибка при создании напоминания.",
                reminders_menu()
            )

        if chat_id in self.states:
            del self.states[chat_id]

    def list_reminders(self, chat_id: int):
        reminders = self.reminder_service.get_user_reminders(chat_id)
        if not reminders:
            self.client.send_message(chat_id, "📭 У вас пока нет напоминаний.", reminders_menu())
            return

        text = "⏰ **Ваши напоминания:**\n\n"
        for r in reminders:
            text += f"🆔 `{r.id}` | 🕐 {r.remind_at} | 📝 {r.text}\n"

        text += "\n❌ Удалить: `/delremind <ID>`"
        self.client.send_message(chat_id, text, reminders_menu(), parse_mode="Markdown")

    def start_delete(self, chat_id: int):
        self.client.send_message(
            chat_id,
            "❌ Введите ID напоминания, которое хотите удалить.\n"
            "Пример: `1`",
            back_menu()
        )
        self.states[chat_id] = {"step": "waiting_delete"}

    def process_delete(self, chat_id: int, text: str):
        try:
            reminder_id = int(text.strip())
        except ValueError:
            self.client.send_message(
                chat_id,
                "❌ Введите корректный ID (число).",
                reminders_menu()
            )
            return

        if self.reminder_service.delete(chat_id, reminder_id):
            self.client.send_message(
                chat_id,
                f"✅ Напоминание #{reminder_id} удалено.",
                reminders_menu()
            )
        else:
            self.client.send_message(
                chat_id,
                f"❌ Напоминание #{reminder_id} не найдено.",
                reminders_menu()
            )

        if chat_id in self.states:
            del self.states[chat_id]

    def process_state(self, chat_id: int, text: str):
        state = self.states.get(chat_id)
        if not state:
            return

        if text == "🔙 Назад":
            if chat_id in self.states:
                del self.states[chat_id]
            self.show_menu(chat_id)
            return

        step = state.get("step")

        if step == "waiting_remind":
            self.process_create(chat_id, text)
        elif step == "waiting_delete":
            self.process_delete(chat_id, text)
