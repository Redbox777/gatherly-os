from bot_core.client import TelegramClient
from services import ChecklistService
from core import Database
from bot_core.keyboards import main_menu

class ChecklistHandler:
    def __init__(self, client: TelegramClient, db: Database):
        self.client = client
        self.checklist_service = ChecklistService(db)
        self.states = {}

    def create_checklist(self, chat_id: int, meeting_id_str: str):
        """Создать чек-лист для встречи: /checklist <ID>"""
        try:
            meeting_id = int(meeting_id_str)
        except ValueError:
            self.client.send_message(chat_id, "❌ Введите корректный ID встречи.", main_menu())
            return

        self.states[chat_id] = {"meeting_id": meeting_id, "step": "add_task"}
        self.client.send_message(
            chat_id,
            f"📝 Добавьте задачу для встречи #{meeting_id}\n"
            f"Или напишите /done чтобы завершить",
            main_menu()
        )

    def add_task(self, chat_id: int, text: str):
        """Добавить задачу в чек-лист"""
        state = self.states.get(chat_id)
        if not state:
            return

        task_id = self.checklist_service.add_task(state["meeting_id"], chat_id, text)
        if task_id > 0:
            self.client.send_message(chat_id, f"✅ Задача добавлена: {text}", main_menu())
            self.show_checklist(chat_id, state["meeting_id"])
        else:
            self.client.send_message(chat_id, "❌ Ошибка добавления задачи.", main_menu())

    def show_checklist(self, chat_id: int, meeting_id: int):
        """Показать чек-лист встречи"""
        tasks = self.checklist_service.get_tasks(meeting_id)
        if not tasks:
            self.client.send_message(chat_id, "📭 Чек-лист пуст.", main_menu())
            return

        text = f"📋 **Чек-лист встречи #{meeting_id}**\n\n"
        for t in tasks:
            status = "✅" if t.done else "⬜"
            text += f"{status} {t.task} (ID: {t.id})\n"

        text += "\n/done <ID> — отметить выполненным\n/delete <ID> — удалить"
        self.client.send_message(chat_id, text, main_menu(), parse_mode="Markdown")

    def toggle_done(self, chat_id: int, task_id_str: str):
        """Отметить задачу как выполненную"""
        try:
            task_id = int(task_id_str)
        except ValueError:
            self.client.send_message(chat_id, "❌ Введите корректный ID задачи.", main_menu())
            return

        if self.checklist_service.toggle_done(task_id, chat_id):
            self.client.send_message(chat_id, f"✅ Статус задачи обновлён.", main_menu())
            # Показываем обновлённый чек-лист
            state = self.states.get(chat_id)
            if state:
                self.show_checklist(chat_id, state["meeting_id"])
        else:
            self.client.send_message(chat_id, "❌ Ошибка или нет прав.", main_menu())
