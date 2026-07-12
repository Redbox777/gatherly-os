import sqlite3
import traceback
from datetime import datetime
from core import get_logger

logger = get_logger(__name__)

class ErrorCollector:
    def __init__(self, db_path: str = "logs/errors.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Создаёт таблицу для ошибок"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                module TEXT,
                function TEXT,
                user_id INTEGER,
                command TEXT,
                error_type TEXT,
                error_message TEXT,
                traceback TEXT,
                resolved INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def add_error(self, error: Exception, user_id: int = None, command: str = None):
        """Добавить ошибку в базу"""
        timestamp = datetime.now().isoformat()
        error_type = type(error).__name__
        error_message = str(error)
        traceback_text = traceback.format_exc()

        # Определяем модуль и функцию
        import inspect
        frame = inspect.currentframe().f_back
        module = frame.f_globals.get('__name__', 'unknown')
        function = frame.f_code.co_name

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO errors (
                timestamp, module, function, user_id, command,
                error_type, error_message, traceback
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            timestamp, module, function, user_id, command,
            error_type, error_message, traceback_text
        ))
        conn.commit()
        conn.close()

        logger.error(f"Ошибка сохранена: {error_type} - {error_message}")

    def get_errors(self, limit: int = 100, resolved: int = 0):
        """Получить ошибки"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM errors
            WHERE resolved = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (resolved, limit))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def mark_resolved(self, error_id: int):
        """Отметить ошибку как исправленную"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE errors SET resolved = 1 WHERE id = ?', (error_id,))
        conn.commit()
        conn.close()

    def get_stats(self):
        """Получить статистику по ошибкам"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM errors')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM errors WHERE resolved = 0')
        unresolved = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT error_type, COUNT(*) as count
            FROM errors
            GROUP BY error_type
            ORDER BY count DESC
        ''')
        by_type = cursor.fetchall()
        
        conn.close()
        return {
            "total": total,
            "unresolved": unresolved,
            "by_type": by_type
        }
