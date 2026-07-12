from core import Database, get_logger
from models import User

logger = get_logger(__name__)

class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    def save(self, user: User) -> None:
        """Сохранить или обновить пользователя"""
        query = """
            INSERT OR REPLACE INTO users (user_id, first_name, username, city, timezone, interests, created_at)
            VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """
        self.db.execute(query, (
            user.user_id,
            user.first_name,
            user.username,
            user.city,
            user.timezone,
            user.interests
        ))

    def get_by_id(self, user_id: int) -> User | None:
        """Получить пользователя по ID"""
        query = "SELECT * FROM users WHERE user_id = ?"
        row = self.db.fetch_one(query, (user_id,))
        return User.from_db(row) if row else None

    def get_all(self) -> list[User]:
        """Получить всех пользователей"""
        query = "SELECT * FROM users ORDER BY created_at DESC"
        rows = self.db.fetch_all(query)
        return [User.from_db(row) for row in rows]

    def update_city(self, user_id: int, city: str) -> None:
        """Обновить город пользователя"""
        query = "UPDATE users SET city = ? WHERE user_id = ?"
        self.db.execute(query, (city, user_id))

    def delete(self, user_id: int) -> None:
        """Удалить пользователя"""
        query = "DELETE FROM users WHERE user_id = ?"
        self.db.execute(query, (user_id,))
