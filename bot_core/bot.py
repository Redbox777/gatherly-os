import time
from core import Database, get_logger
from .client import TelegramClient
from .dispatcher import Dispatcher

logger = get_logger(__name__)

class Bot:
    def __init__(self, config):
        self.config = config
        self.client = TelegramClient(config.bot.token)
        self.db = Database(config)
        self.dispatcher = Dispatcher(self.client, self.db)
        self.running = False

    def run(self):
        logger.info("🤖 Бот запущен")
        self.running = True
        last_update_id = 0
        last_reminder_check = 0

        while self.running:
            try:
                # Получение обновлений
                updates = self.client.get_updates(last_update_id + 1)
                for update in updates:
                    last_update_id = update.get("update_id", 0)
                    self.dispatcher.process_update(update)
                
                # Проверка напоминаний каждые 30 секунд
                now = int(time.time())
                if now - last_reminder_check >= 30:
                    last_reminder_check = now
                    self._check_reminders()
                
                time.sleep(1)
            except Exception as e:
                logger.error(f"❌ Ошибка: {e}")
                time.sleep(5)

    def _check_reminders(self):
        """Проверка и отправка напоминаний"""
        try:
            from services import ReminderService
            reminder_service = ReminderService(self.db)
            reminder_service.check_and_send(self.client.send_message)
        except Exception as e:
            logger.error(f"Ошибка при проверке напоминаний: {e}")

    def stop(self):
        self.running = False
        logger.info("👋 Бот остановлен")
