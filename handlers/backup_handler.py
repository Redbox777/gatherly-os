from bot_core.client import TelegramClient
from services import BackupService
from core import Database
from bot_core.keyboards import main_menu

class BackupHandler:
    def __init__(self, client: TelegramClient, db: Database):
        self.client = client
        self.backup_service = BackupService()

    def create_backup(self, chat_id: int):
        """Создать бэкап"""
        try:
            path = self.backup_service.create_backup()
            self.client.send_message(chat_id, f"✅ Бэкап создан: `{path}`", main_menu(), parse_mode="Markdown")
        except Exception as e:
            self.client.send_message(chat_id, f"❌ Ошибка бэкапа: {e}", main_menu())

    def list_backups(self, chat_id: int):
        """Показать список бэкапов"""
        backups = self.backup_service.list_backups()
        if not backups:
            self.client.send_message(chat_id, "📭 Бэкапов пока нет.", main_menu())
            return

        text = "📂 **Список бэкапов:**\n\n"
        for b in backups[:10]:
            text += f"• `{b}`\n"
        text += f"\nВсего: {len(backups)} бэкапов"
        self.client.send_message(chat_id, text, main_menu(), parse_mode="Markdown")
