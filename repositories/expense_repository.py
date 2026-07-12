from core import Database
from models import Expense

class ExpenseRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(self, expense: Expense) -> int:
        query = """
            INSERT INTO expenses (meeting_id, user_id, amount, description, created_at)
            VALUES (?, ?, ?, ?, datetime('now'))
        """
        cursor = self.db.execute(query, (
            expense.meeting_id,
            expense.user_id,
            expense.amount,
            expense.description
        ))
        return cursor.lastrowid

    def get_by_meeting(self, meeting_id: int) -> list[Expense]:
        query = "SELECT * FROM expenses WHERE meeting_id = ? ORDER BY created_at DESC"
        rows = self.db.fetch_all(query, (meeting_id,))
        return [Expense.from_db(row) for row in rows]

    def get_by_user(self, user_id: int) -> list[Expense]:
        query = "SELECT * FROM expenses WHERE user_id = ? ORDER BY created_at DESC"
        rows = self.db.fetch_all(query, (user_id,))
        return [Expense.from_db(row) for row in rows]

    def get_total_by_meeting(self, meeting_id: int) -> float:
        query = "SELECT SUM(amount) as total FROM expenses WHERE meeting_id = ?"
        row = self.db.fetch_one(query, (meeting_id,))
        return row["total"] if row and row["total"] else 0.0
