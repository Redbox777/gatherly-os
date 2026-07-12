from bot_core.client import TelegramClient
from services import StatsService
from core import Database
from bot_core.keyboards import main_menu

class StatsHandler:
    def __init__(self, client: TelegramClient, db: Database):
        self.client = client
        self.stats_service = StatsService(db)

    def show_user_stats(self, chat_id: int):
        """Показать статистику пользователя"""
        stats = self.stats_service.get_user_stats(chat_id)
        activity = self.stats_service.get_activity_stats(7)

        text = f"""
📊 **Твоя статистика**

📅 **Встречи**
• Создано: {stats['meetings_created']}
• Участий: {stats['meetings_participated']}

👥 **Социальное**
• Друзей: {stats['friends']}

💰 **Расходы**
• Всего трат: {stats['expenses_count']}
• Общая сумма: {stats['total_expenses']:.2f}

⏰ **Напоминания**
• Активных: {stats['reminders']}

📈 **За последние 7 дней**
• Новых встреч: {activity['new_meetings']}
• Новых пользователей: {activity['new_users']}
"""
        self.client.send_message(chat_id, text, main_menu(), parse_mode="Markdown")

    def show_global_stats(self, chat_id: int):
        """Показать общую статистику (только админ)"""
        from config import ADMIN_ID
        if chat_id != ADMIN_ID:
            self.client.send_message(chat_id, "⛔ Только для администратора.", main_menu())
            return

        stats = self.stats_service.get_global_stats()
        activity = self.stats_service.get_activity_stats(30)

        text = f"""
📊 **Глобальная статистика**

👤 **Пользователи**: {stats['users']}

📅 **Встречи**
• Всего: {stats['meetings']}

👥 **Социальное**
• Дружеских связей: {stats['friendships']}

💰 **Расходы**
• Всего расходов: {stats['expenses']}
• Общая сумма: {stats['total_amount']:.2f}

⏰ **Напоминания**: {stats['reminders']}

📈 **За последние 30 дней**
• Новых встреч: {activity['new_meetings']}
• Новых пользователей: {activity['new_users']}
"""
        self.client.send_message(chat_id, text, main_menu(), parse_mode="Markdown")
