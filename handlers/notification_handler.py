from bot_core.client import TelegramClient
from services import MeetingService
from core import Database
from bot_core.keyboards import main_menu

class NotificationHandler:
    def __init__(self, client: TelegramClient, db: Database):
        self.client = client
        self.meeting_service = MeetingService(db)

    def notify_all(self, chat_id: int, text: str):
        """Уведомить всех участников встречи: /notify <ID> <текст>"""
        parts = text.split(maxsplit=2)
        if len(parts) < 3:
            self.client.send_message(
                chat_id,
                "❌ Формат: /notify <ID> <текст>",
                main_menu()
            )
            return

        try:
            meeting_id = int(parts[1])
            message = parts[2]
        except ValueError:
            self.client.send_message(chat_id, "❌ Введите корректный ID встречи.", main_menu())
            return

        meeting = self.meeting_service.get_meeting(meeting_id)
        if "error" in meeting:
            self.client.send_message(chat_id, "❌ Встреча не найдена или нет доступа.", main_menu())
            return

        # Отправляем уведомление всем участникам
        all_participants = meeting['going'] + meeting['maybe'] + meeting['not_going']
        sent_count = 0

        for user_id in set(all_participants):
            if user_id != chat_id:
                self.client.send_message(
                    user_id,
                    f"📢 **Уведомление о встрече #{meeting_id}**\n"
                    f"📌 {meeting['title']}\n"
                    f"👤 От: {chat_id}\n"
                    f"📝 {message}",
                    main_menu(),
                    parse_mode="Markdown"
                )
                sent_count += 1

        self.client.send_message(
            chat_id,
            f"✅ Уведомление отправлено {sent_count} участникам.",
            main_menu()
        )
