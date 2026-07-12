from core import Database, get_logger
from datetime import datetime, timedelta

logger = get_logger(__name__)

class StatsService:
    def __init__(self, db: Database):
        self.db = db

    def get_user_stats(self, user_id: int) -> dict:
        """Статистика пользователя"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM meetings WHERE creator_id = ?", (user_id,))
            meetings_created = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM meeting_participants WHERE user_id = ?", (user_id,))
            meetings_participated = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM friends WHERE user_id = ? AND status = 'accepted'", (user_id,))
            friends_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM expenses WHERE user_id = ?", (user_id,))
            expenses_count = cursor.fetchone()[0]

            cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,))
            total_expenses = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(*) FROM reminders WHERE user_id = ?", (user_id,))
            reminders_count = cursor.fetchone()[0]

        return {
            "meetings_created": meetings_created,
            "meetings_participated": meetings_participated,
            "friends": friends_count,
            "expenses_count": expenses_count,
            "total_expenses": total_expenses,
            "reminders": reminders_count
        }

    def get_global_stats(self) -> dict:
        """Общая статистика по боту"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM users")
            users = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM meetings")
            meetings = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM friends WHERE status = 'accepted'")
            friendships = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM expenses")
            expenses = cursor.fetchone()[0]

            cursor.execute("SELECT SUM(amount) FROM expenses")
            total_amount = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(*) FROM reminders")
            reminders = cursor.fetchone()[0]

        return {
            "users": users,
            "meetings": meetings,
            "friendships": friendships,
            "expenses": expenses,
            "total_amount": total_amount,
            "reminders": reminders
        }

    def get_activity_stats(self, days: int = 7) -> dict:
        """Статистика активности за последние N дней"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            since = (datetime.now() - timedelta(days=days)).isoformat()
            
            cursor.execute("SELECT COUNT(*) FROM meetings WHERE created_at > ?", (since,))
            meetings = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM users WHERE created_at > ?", (since,))
            new_users = cursor.fetchone()[0]

        return {
            "new_meetings": meetings,
            "new_users": new_users,
            "days": days
        }
