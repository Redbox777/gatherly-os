from bot_core.client import TelegramClient
from services import UserService
from core import Database
from bot_core.keyboards import main_menu, back_menu

class ProfileHandler:
    def __init__(self, client: TelegramClient, db: Database):
        self.client = client
        self.user_service = UserService(db)
        self.states = {}

    def show_profile(self, chat_id: int):
        """Показать профиль"""
        profile = self.user_service.get_profile(chat_id)
        if "error" in profile:
            self.client.send_message(chat_id, profile["error"], main_menu())
            return
        
        text = (
            f"👤 **Профиль**\n\n"
            f"📛 Имя: {profile['first_name']}\n"
            f"🔹 Юзернейм: @{profile['username']}\n"
            f"🆔 ID: {profile['user_id']}\n\n"
            f"🌍 Город: {profile['city']}\n"
            f"🕐 Часовой пояс: {profile['timezone']}\n"
            f"🎯 Интересы: {profile['interests']}"
        )
        self.client.send_message(chat_id, text, main_menu())

    def edit_city(self, chat_id: int):
        """Начать редактирование города"""
        self.client.send_message(chat_id, "🏙 Введите ваш город (или '-' чтобы пропустить):", back_menu())
        self.states[chat_id] = "waiting_city"

    def edit_interests(self, chat_id: int):
        """Начать редактирование интересов"""
        self.client.send_message(chat_id, "🎯 Введите ваши интересы (через запятую):", back_menu())
        self.states[chat_id] = "waiting_interests"

    def process_state(self, chat_id: int, text: str):
        """Обработка состояний редактирования"""
        state = self.states.get(chat_id)
        
        if state == "waiting_city":
            if text and text != "-":
                self.user_service.update_city(chat_id, text)
                self.client.send_message(chat_id, f"✅ Город '{text}' сохранён!", main_menu())
            else:
                self.client.send_message(chat_id, "⏭ Город пропущен.", main_menu())
            del self.states[chat_id]
        
        elif state == "waiting_interests":
            if text and text != "-":
                self.user_service.update_interests(chat_id, text)
                self.client.send_message(chat_id, f"✅ Интересы сохранены!", main_menu())
            else:
                self.client.send_message(chat_id, "⏭ Интересы пропущены.", main_menu())
            del self.states[chat_id]
