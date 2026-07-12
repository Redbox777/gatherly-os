from datetime import datetime
from core import Database, get_logger
from repositories import FriendRepository, UserRepository
from models import Friend

logger = get_logger(__name__)

class FriendService:
    def __init__(self, db: Database):
        self.db = db
        self.friend_repo = FriendRepository(db)
        self.user_repo = UserRepository(db)

    def send_request(self, user_id: int, friend_id: int) -> dict:
        """Отправить заявку в друзья"""
        if user_id == friend_id:
            return {"error": "Нельзя добавить себя"}
        
        # Проверяем, существует ли пользователь
        friend = self.user_repo.get_by_id(friend_id)
        if not friend:
            return {"error": "Пользователь не найден"}
        
        # Проверяем, есть ли уже заявка
        existing = self.friend_repo.get_friendship(user_id, friend_id)
        if existing:
            if existing.status == "accepted":
                return {"error": "Уже друзья"}
            elif existing.status == "pending":
                return {"error": "Заявка уже отправлена"}
        
        self.friend_repo.add_friend(user_id, friend_id, "pending")
        self.friend_repo.add_friend(friend_id, user_id, "pending")
        logger.info(f"Заявка в друзья: {user_id} -> {friend_id}")
        return {"success": True}

    def accept_request(self, user_id: int, friend_id: int) -> bool:
        """Принять заявку в друзья"""
        friendship = self.friend_repo.get_friendship(user_id, friend_id)
        if not friendship or friendship.status != "pending":
            return False
        
        self.friend_repo.update_status(user_id, friend_id, "accepted")
        self.friend_repo.update_status(friend_id, user_id, "accepted")
        logger.info(f"Заявка принята: {user_id} <-> {friend_id}")
        return True

    def reject_request(self, user_id: int, friend_id: int) -> bool:
        """Отклонить заявку"""
        friendship = self.friend_repo.get_friendship(user_id, friend_id)
        if not friendship or friendship.status != "pending":
            return False
        
        self.friend_repo.update_status(user_id, friend_id, "rejected")
        self.friend_repo.update_status(friend_id, user_id, "rejected")
        return True

    def get_friends(self, user_id: int) -> list:
        """Получить список друзей"""
        return self.friend_repo.get_friends(user_id)

    def get_pending_requests(self, user_id: int) -> list:
        """Получить входящие заявки"""
        return self.friend_repo.get_pending_requests(user_id)

