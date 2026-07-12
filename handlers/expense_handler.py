from bot_core.client import TelegramClient
from services import ExpenseService
from core import Database
from bot_core.keyboards import main_menu, back_menu

class ExpenseHandler:
    def __init__(self, client: TelegramClient, db: Database):
        self.client = client
        self.expense_service = ExpenseService(db)
        self.states = {}

    def add_expense(self, chat_id: int, meeting_id_str: str):
        """Начать добавление расхода"""
        try:
            meeting_id = int(meeting_id_str)
        except ValueError:
            self.client.send_message(chat_id, "❌ Введите корректный ID встречи.", main_menu())
            return
        
        self.states[chat_id] = {"meeting_id": meeting_id, "step": "amount"}
        self.client.send_message(chat_id, "💰 Введите сумму расхода:", back_menu())

    def list_expenses(self, chat_id: int, meeting_id_str: str):
        """Показать расходы по встрече"""
        try:
            meeting_id = int(meeting_id_str)
        except ValueError:
            self.client.send_message(chat_id, "❌ Введите корректный ID встречи.", main_menu())
            return
        
        expenses = self.expense_service.get_meeting_expenses(meeting_id)
        
        if not expenses:
            self.client.send_message(chat_id, "📭 Нет расходов для этой встречи.", main_menu())
            return
        
        total = self.expense_service.get_total_by_meeting(meeting_id)
        
        text = f"💰 **Расходы по встрече #{meeting_id}**\n\n"
        for e in expenses:
            text += f"💵 {e.amount} руб. — {e.description or 'Без описания'} (от {e.user_id})\n"
        
        text += f"\n📊 **Итого: {total} руб.**"
        
        self.client.send_message(chat_id, text, main_menu())

    def process_state(self, chat_id: int, text: str):
        """Обработка пошагового добавления расхода"""
        state = self.states.get(chat_id)
        if not state:
            return
        
        if state["step"] == "amount":
            try:
                amount = float(text.replace(",", "."))
            except ValueError:
                self.client.send_message(chat_id, "❌ Введите корректную сумму (например: 150.50):", back_menu())
                return
            
            state["amount"] = amount
            state["step"] = "description"
            self.client.send_message(chat_id, "📝 Введите описание расхода (или '-' чтобы пропустить):", back_menu())
        
        elif state["step"] == "description":
            description = text if text != "-" else None
            
            expense_id = self.expense_service.add_expense(
                meeting_id=state["meeting_id"],
                user_id=chat_id,
                amount=state["amount"],
                description=description
            )
            
            if expense_id > 0:
                self.client.send_message(chat_id, f"✅ Расход добавлен! ID: {expense_id}", main_menu())
            else:
                self.client.send_message(chat_id, "❌ Ошибка при добавлении расхода.", main_menu())
            
            del self.states[chat_id]
