from core import Database
from models import Friend

class FriendRepository:
    def __init__(self, db: Database):
        self.db = db

    def add_friend(self, user_id: int, friend_id: int, status: str) -> None:
        query = """
            INSERT OR REPLACE INTO friends (user_id, friend_id, status, created_at)
            VALUES (?, ?, ?, datetime('now'))
        """
        self.db.execute(query, (user_id, friend_id, status))

    def get_friendship(self, user_id: int, friend_id: int) -> Friend | None:
        query = "SELECT * FROM friends WHERE user_id = ? AND friend_id = ?"
        row = self.db.fetch_one(query, (user_id, friend_id))
        return Friend.from_db(row) if row else None

    def update_status(self, user_id: int, friend_id: int, status: str) -> None:
        query = "UPDATE friends SET status = ? WHERE user_id = ? AND friend_id = ?"
        self.db.execute(query, (status, user_id, friend_id))

    def get_friends(self, user_id: int) -> list[Friend]:
        query = "SELECT * FROM friends WHERE user_id = ? AND status = 'accepted'"
        rows = self.db.fetch_all(query, (user_id,))
        return [Friend.from_db(row) for row in rows]

    def get_pending_requests(self, user_id: int) -> list[Friend]:
        query = "SELECT * FROM friends WHERE user_id = ? AND status = 'pending'"
        rows = self.db.fetch_all(query, (user_id,))
        return [Friend.from_db(row) for row in rows]
