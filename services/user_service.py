from core import Database, get_logger
from repositories import UserRepository
from models import User

logger = get_logger(__name__)

class UserService:
    def __init__(self, db: Database):
        self.db = db
        self.repo = UserRepository(db)

    def register_or_update(self, user_id: int, first_name: str, username: str = None) -> User:
        """Регистрация или обновление пользователя"""
        user = self.repo.get_by_id(user_id)
        if user:
            # Обновляем только если изменилось имя или username
            if user.first_name != first_name or user.username != username:
                user.first_name = first_name
                user.username = username
                self.repo.save(user)
            return user
        
        # Новый пользователь
        new_user = User(
            user_id=user_id,
            first_name=first_name,
            username=username
        )
        self.repo.save(new_user)
        logger.info(f"Новый пользователь: {first_name} ({user_id})")
        return new_user

    def get_profile(self, user_id: int) -> dict:
        """Получить профиль пользователя"""
        user = self.repo.get_by_id(user_id)
        if not user:
            return {"error": "Пользователь не найден"}
        
        return {
            "user_id": user.user_id,
            "first_name": user.first_name,
            "username": user.username or "нет",
            "city": user.city or "—",
            "timezone": user.timezone or "—",
            "interests": user.interests or "—"
        }

    def update_city(self, user_id: int, city: str) -> bool:
        """Обновить город пользователя"""
        user = self.repo.get_by_id(user_id)
        if not user:
            return False
        user.city = city
        self.repo.save(user)
        return True

    def update_interests(self, user_id: int, interests: str) -> bool:
        """Обновить интересы пользователя"""
        user = self.repo.get_by_id(user_id)
        if not user:
            return False
        user.interests = interests
        self.repo.save(user)
        return True
