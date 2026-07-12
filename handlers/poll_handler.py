from bot_core.client import TelegramClient
from services import PollService
from core import Database
from bot_core.keyboards import main_menu

class PollHandler:
    def __init__(self, client: TelegramClient, db: Database):
        self.client = client
        self.poll_service = PollService(db)
        self.states = {}

    def create_poll(self, chat_id: int, text: str):
        """Создать опрос: /poll <ID> <вопрос> <вариант1> <вариант2> ..."""
        parts = text.split(maxsplit=3)
        if len(parts) < 4:
            self.client.send_message(
                chat_id,
                "❌ Формат: /poll <ID> <вопрос> <вариант1> <вариант2> ...",
                main_menu()
            )
            return

        try:
            meeting_id = int(parts[1])
            question = parts[2]
            options = parts[3].split(',')
        except ValueError:
            self.client.send_message(chat_id, "❌ Введите корректный ID встречи.", main_menu())
            return

        if len(options) < 2:
            self.client.send_message(chat_id, "❌ Нужно минимум 2 варианта.", main_menu())
            return

        poll_id = self.poll_service.create_poll(meeting_id, chat_id, question, options)
        if poll_id < 0:
            self.client.send_message(chat_id, "❌ Ошибка создания опроса.", main_menu())
            return

        # Показываем опрос
        self.show_poll(chat_id, poll_id)

    def show_poll(self, chat_id: int, poll_id: int):
        """Показать опрос с кнопками"""
        from services import PollService
        poll_service = PollService(self.db)
        polls = poll_service.poll_repo.get_by_id(poll_id)
        if not polls:
            self.client.send_message(chat_id, "❌ Опрос не найден.", main_menu())
            return

        options = polls.options.split(',')
        text = f"📊 **Опрос #{polls.id}**\n{polls.question}\n\n"
        keyboard = []

        for i, opt in enumerate(options):
            text += f"{i+1}. {opt}\n"
            keyboard.append([{"text": opt, "callback_data": f"poll_{poll_id}_{i}"}])

        self.client.send_message(chat_id, text, {"inline_keyboard": keyboard}, parse_mode="Markdown")
