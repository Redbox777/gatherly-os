from datetime import datetime, timedelta
from core import get_logger
from .error_collector import ErrorCollector

logger = get_logger(__name__)

class ReportGenerator:
    def __init__(self):
        self.collector = ErrorCollector()

    def generate_daily_report(self) -> str:
        """Создать текстовый отчёт за день"""
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Получаем ошибки за сегодня
        errors = self.collector.get_errors(limit=1000)
        today_errors = [e for e in errors if e['timestamp'].startswith(today)]
        
        # Статистика
        stats = self.collector.get_stats()
        
        # Формируем отчёт
        report = f"""
📊 **ОТЧЁТ ПО ОШИБКАМ: {today}**
{'─' * 40}

📈 **СТАТИСТИКА**
• Всего ошибок: {stats['total']}
• Неисправлено: {stats['unresolved']}
• Исправлено: {stats['total'] - stats['unresolved']}

📋 **ОШИБКИ ПО ТИПАМ**
"""
        for error_type, count in stats['by_type']:
            report += f"• {error_type}: {count}\n"

        if today_errors:
            report += f"\n🔴 **ОШИБКИ ЗА СЕГОДНЯ ({len(today_errors)})**\n"
            for e in today_errors[:10]:
                report += f"""
• {e['timestamp'][:19]} | {e['user_id'] or 'None'} | {e['command'] or 'unknown'}
  {e['error_type']}: {e['error_message'][:100]}
"""
        else:
            report += "\n✅ **Ошибок за сегодня нет!**\n"

        report += f"""
{'─' * 40}
📌 *Отчёт создан автоматически*
"""
        return report

    def save_report(self, report: str):
        """Сохранить отчёт в файл"""
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"analytics/report_{today}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        
        logger.info(f"Отчёт сохранён: {filename}")
        return filename
