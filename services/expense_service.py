from core import Database, get_logger
from repositories import ExpenseRepository, MeetingRepository
from models import Expense

logger = get_logger(__name__)

class ExpenseService:
    def __init__(self, db: Database):
        self.db = db
        self.expense_repo = ExpenseRepository(db)
        self.meeting_repo = MeetingRepository(db)

    def add_expense(self, meeting_id: int, user_id: int, amount: float, description: str = None) -> int:
        """Добавить расход на встречу"""
        meeting = self.meeting_repo.get_by_id(meeting_id)
        if not meeting:
            return -1
        
        expense = Expense(
            id=0,
            meeting_id=meeting_id,
            user_id=user_id,
            amount=amount,
            description=description
        )
        expense_id = self.expense_repo.create(expense)
        logger.info(f"Добавлен расход #{expense_id}: {amount} ({description})")
        return expense_id

    def get_meeting_expenses(self, meeting_id: int) -> list:
        """Получить все расходы по встрече"""
        return self.expense_repo.get_by_meeting(meeting_id)

    def get_user_expenses(self, user_id: int) -> list:
        """Получить все расходы пользователя"""
        return self.expense_repo.get_by_user(user_id)

    def get_total_by_meeting(self, meeting_id: int) -> float:
        """Получить общую сумму расходов по встрече"""
        return self.expense_repo.get_total_by_meeting(meeting_id)
