from bot_core.client import TelegramClient
from services import UserService
from core import Database
from bot_core.keyboards import main_menu

class StartHandler:
    def __init__(self, client: TelegramClient, db: Database):
        self.client = client
        self.user_service = UserService(db)

    def handle(self, chat_id: int, first_name: str, username: str = None):
        """Обработчик /start"""
        # Регистрируем пользователя
        user = self.user_service.register_or_update(chat_id, first_name, username)

        text = f"""
👋 Добро пожаловать в Gatherly OS!

👤 Пользователь: {first_name}
🆔 ID: {chat_id}

─────────────────────

💡 Что я умею:
• 🌤 Погода — узнавай погоду в любом городе
• 📅 Встречи — создавай и управляй встречами
• 👥 Друзья — добавляй друзей и общайся
• 💰 Расходы — считай общие траты
• ⏰ Напоминания — ничего не забывай
• 📆 Календарь — планируй даты
• 📊 Опросы — собирай мнения
• 📋 Чек-листы — контролируй задачи
• 💬 Чаты — обсуждай в группах
• 📊 Статистика — анализируй активность

─────────────────────

Используй меню ниже или команды /help
"""
        self.client.send_message(chat_id, text, main_menu())
