from bot_core.client import TelegramClient
from services import FriendService
from core import Database
from bot_core.keyboards import main_menu

class FriendHandler:
    def __init__(self, client: TelegramClient, db: Database):
        self.client = client
        self.friend_service = FriendService(db)

    def add_friend(self, chat_id: int, friend_id_str: str):
        """Добавить друга по ID"""
        try:
            friend_id = int(friend_id_str)
        except ValueError:
            self.client.send_message(chat_id, "❌ Введите корректный ID пользователя.", main_menu())
            return
        
        result = self.friend_service.send_request(chat_id, friend_id)
        if "error" in result:
            self.client.send_message(chat_id, f"❌ {result['error']}", main_menu())
        else:
            self.client.send_message(chat_id, f"✅ Заявка отправлена пользователю {friend_id}", main_menu())

    def list_friends(self, chat_id: int):
        """Показать список друзей"""
        friends = self.friend_service.get_friends(chat_id)
        
        if not friends:
            self.client.send_message(chat_id, "📭 У вас пока нет друзей.", main_menu())
            return
        
        text = "👥 **Ваши друзья:**\n\n"
        for f in friends:
            text += f"🔹 {f.friend_id}\n"
        
        self.client.send_message(chat_id, text, main_menu())

    def list_requests(self, chat_id: int):
        """Показать входящие заявки"""
        requests = self.friend_service.get_pending_requests(chat_id)
        
        if not requests:
            self.client.send_message(chat_id, "📭 Нет входящих заявок.", main_menu())
            return
        
        text = "📨 **Входящие заявки:**\n\n"
        for r in requests:
            text += f"🔹 От пользователя {r.user_id}\n"
            text += f"  /accept {r.user_id} — принять\n"
            text += f"  /reject {r.user_id} — отклонить\n\n"
        
        self.client.send_message(chat_id, text, main_menu())

    def accept_request(self, chat_id: int, friend_id_str: str):
        """Принять заявку"""
        try:
            friend_id = int(friend_id_str)
        except ValueError:
            self.client.send_message(chat_id, "❌ Введите корректный ID.", main_menu())
            return
        
        if self.friend_service.accept_request(chat_id, friend_id):
            self.client.send_message(chat_id, f"✅ Заявка от {friend_id} принята!", main_menu())
        else:
            self.client.send_message(chat_id, "❌ Ошибка при принятии заявки.", main_menu())

    def reject_request(self, chat_id: int, friend_id_str: str):
        """Отклонить заявку"""
        try:
            friend_id = int(friend_id_str)
        except ValueError:
            self.client.send_message(chat_id, "❌ Введите корректный ID.", main_menu())
            return
        
        if self.friend_service.reject_request(chat_id, friend_id):
            self.client.send_message(chat_id, f"✅ Заявка от {friend_id} отклонена.", main_menu())
        else:
            self.client.send_message(chat_id, "❌ Ошибка при отклонении.", main_menu())
