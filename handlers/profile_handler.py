from bot_core.client import TelegramClient
from services import UserService
from core import Database
from bot_core.keyboards import main_menu, profile_menu, back_menu

class ProfileHandler:
    def __init__(self, client: TelegramClient, db: Database):
        self.client = client
        self.user_service = UserService(db)
        self.states = {}

    def show_profile(self, chat_id: int):
        profile = self.user_service.get_profile(chat_id)
        if "error" in profile:
            self.client.send_message(chat_id, profile["error"], main_menu())
            return

        text = f"""
👤 **ПРОФИЛЬ**

━━━━━━━━━━━━━━━━━━

📛 **Имя:** {profile['first_name']}
🔹 **Юзернейм:** @{profile['username'] or 'нет'}
🆔 **ID:** `{profile['user_id']}`

━━━━━━━━━━━━━━━━━━

🌍 **Город:** {profile['city'] or '—'}
🎯 **Интересы:** {profile['interests'] or '—'}

━━━━━━━━━━━━━━━━━━

💡 *Нажми «✏️ Город» или «🎯 Интересы» для изменения*
"""
        self.client.send_message(chat_id, text, profile_menu(), parse_mode="Markdown")

    def edit_city(self, chat_id: int):
        self.client.send_message(chat_id, "🌍 Введите ваш город:", back_menu())
        self.states[chat_id] = "waiting_city"

    def edit_interests(self, chat_id: int):
        self.client.send_message(chat_id, "🎯 Введите ваши интересы (через запятую):", back_menu())
        self.states[chat_id] = "waiting_interests"

    def process_state(self, chat_id: int, text: str):
        state = self.states.get(chat_id)
        if not state:
            return

        if text == "🔙 Назад":
            if chat_id in self.states:
                del self.states[chat_id]
            self.show_profile(chat_id)
            return

        if state == "waiting_city":
            if text and text != "-":
                self.user_service.update_city(chat_id, text)
                self.client.send_message(chat_id, f"✅ Город обновлён: **{text}**", profile_menu(), parse_mode="Markdown")
            else:
                self.client.send_message(chat_id, "⏭ Город не изменён.", profile_menu())
            del self.states[chat_id]
            self.show_profile(chat_id)

        elif state == "waiting_interests":
            if text and text != "-":
                self.user_service.update_interests(chat_id, text)
                self.client.send_message(chat_id, f"✅ Интересы обновлены: **{text}**", profile_menu(), parse_mode="Markdown")
            else:
                self.client.send_message(chat_id, "⏭ Интересы не изменены.", profile_menu())
            del self.states[chat_id]
            self.show_profile(chat_id)
