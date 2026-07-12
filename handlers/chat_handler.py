from bot_core.client import TelegramClient
from services import ChatService
from core import Database
from bot_core.keyboards import main_menu

class ChatHandler:
    def __init__(self, client: TelegramClient, db: Database):
        self.client = client
        self.chat_service = ChatService(db)

    def enter_chat(self, chat_id: int, meeting_id_str: str):
        """Войти в чат встречи"""
        try:
            meeting_id = int(meeting_id_str)
        except ValueError:
            self.client.send_message(chat_id, "❌ Введите корректный ID встречи.", main_menu())
            return

        # Проверяем, есть ли доступ
        from services import MeetingService
        meeting_service = MeetingService(self.db)
        meeting = meeting_service.get_meeting(meeting_id)
        if "error" in meeting:
            self.client.send_message(chat_id, "❌ Встреча не найдена или нет доступа.", main_menu())
            return

        self.client.send_message(
            chat_id,
            f"💬 Вы вошли в чат встречи #{meeting_id}\n\n"
            f"📌 {meeting['title']}\n"
            f"📝 Пишите сообщения, они будут видны всем участникам.\n\n"
            f"Чтобы выйти из чата, напишите /leave",
            main_menu()
        )

    def send_chat_message(self, chat_id: int, meeting_id_str: str, message: str):
        """Отправить сообщение в чат встречи"""
        try:
            meeting_id = int(meeting_id_str)
        except ValueError:
            self.client.send_message(chat_id, "❌ Введите корректный ID встречи.", main_menu())
            return

        if not message.strip():
            self.client.send_message(chat_id, "❌ Сообщение не может быть пустым.", main_menu())
            return

        # Проверяем участника
        from services import MeetingService
        meeting_service = MeetingService(self.db)
        meeting = meeting_service.get_meeting(meeting_id)
        if "error" in meeting:
            self.client.send_message(chat_id, "❌ Встреча не найдена или нет доступа.", main_menu())
            return

        # Отправляем сообщение
        if self.chat_service.send_message(meeting_id, chat_id, message):
            # Отправляем всем участникам
            for user_id in meeting['going'] + meeting['maybe']:
                if user_id != chat_id:
                    self.client.send_message(
                        user_id,
                        f"💬 Новое сообщение в чате встречи #{meeting_id}\n"
                        f"📌 {meeting['title']}\n"
                        f"👤 От: {chat_id}\n"
                        f"📝 {message}"
                    )
            self.client.send_message(chat_id, "✅ Сообщение отправлено всем участникам.", main_menu())
        else:
            self.client.send_message(chat_id, "❌ Ошибка отправки сообщения.", main_menu())

    def get_chat_history(self, chat_id: int, meeting_id_str: str):
        """Показать историю чата"""
        try:
            meeting_id = int(meeting_id_str)
        except ValueError:
            self.client.send_message(chat_id, "❌ Введите корректный ID встречи.", main_menu())
            return

        messages = self.chat_service.get_chat(meeting_id)
        if not messages:
            self.client.send_message(chat_id, "📭 В чате пока нет сообщений.", main_menu())
            return

        text = f"💬 **История чата встречи #{meeting_id}**\n\n"
        for m in messages[:20]:  # Последние 20 сообщений
            text += f"👤 {m.user_id}: {m.message}\n"

        self.client.send_message(chat_id, text, main_menu(), parse_mode="Markdown")
