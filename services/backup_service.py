import shutil
import os
from datetime import datetime
from core import get_logger

logger = get_logger(__name__)

class BackupService:
    def __init__(self, db_path: str = "gatherly.db", backup_dir: str = "backups"):
        self.db_path = db_path
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)

    def create_backup(self) -> str:
        """Создаёт бэкап базы данных"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{self.backup_dir}/gatherly_{timestamp}.db"
        shutil.copy2(self.db_path, backup_path)
        logger.info(f"Бэкап создан: {backup_path}")
        return backup_path

    def list_backups(self) -> list:
        """Возвращает список всех бэкапов"""
        files = os.listdir(self.backup_dir)
        backups = [f for f in files if f.startswith("gatherly_") and f.endswith(".db")]
        return sorted(backups, reverse=True)

    def restore_backup(self, filename: str) -> bool:
        """Восстанавливает бэкап"""
        backup_path = os.path.join(self.backup_dir, filename)
        if not os.path.exists(backup_path):
            return False
        shutil.copy2(backup_path, self.db_path)
        logger.info(f"Бэкап восстановлен: {filename}")
        return True
