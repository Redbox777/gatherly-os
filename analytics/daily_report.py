import time
import threading
from datetime import datetime
from core import get_logger
from .report_generator import ReportGenerator
from .error_collector import ErrorCollector

logger = get_logger(__name__)

class DailyReport:
    def __init__(self, bot_client, admin_id: int):
        self.bot_client = bot_client
        self.admin_id = admin_id
        self.report_gen = ReportGenerator()
        self.collector = ErrorCollector()
        self.running = False

    def start(self):
        """Запустить ежедневную отправку отчётов"""
        self.running = True
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()
        logger.info("📊 Ежедневные отчёты запущены")

    def _run(self):
        """Цикл проверки времени"""
        while self.running:
            now = datetime.now()
            # Отправка в 23:59 каждый день
            if now.hour == 23 and now.minute == 59:
                self.send_report()
                time.sleep(60)
            time.sleep(30)

    def send_report(self):
        """Сгенерировать и отправить отчёт"""
        report = self.report_gen.generate_daily_report()
        filename = self.report_gen.save_report(report)
        
        # Отправляем отчёт админу
        self.bot_client.send_message(
            self.admin_id,
            f"📊 **Ежедневный отчёт по ошибкам**\n\n{report}",
            parse_mode="Markdown"
        )
        
        logger.info(f"📊 Отчёт отправлен админу {self.admin_id}")

    def stop(self):
        self.running = False
