import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, List, Optional
from .config import Config
from .logger import get_logger

logger = get_logger(__name__)

class Database:
    def __init__(self, config: Config):
        self.db_path = config.database.path
        self._init_tables()

    def _init_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Пользователи
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                username TEXT,
                city TEXT,
                timezone TEXT,
                interests TEXT,
                created_at TEXT
            )''')
            
            # Встречи
            cursor.execute('''CREATE TABLE IF NOT EXISTS meetings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creator_id INTEGER,
                title TEXT,
                description TEXT,
                date TEXT,
                time TEXT,
                place TEXT,
                status TEXT,
                created_at TEXT
            )''')
            
            # Участники встреч
            cursor.execute('''CREATE TABLE IF NOT EXISTS meeting_participants (
                meeting_id INTEGER,
                user_id INTEGER,
                status TEXT,
                PRIMARY KEY (meeting_id, user_id)
            )''')
            
            # Друзья
            cursor.execute('''CREATE TABLE IF NOT EXISTS friends (
                user_id INTEGER,
                friend_id INTEGER,
                status TEXT,
                created_at TEXT,
                PRIMARY KEY (user_id, friend_id)
            )''')
            
            # Расходы
            cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meeting_id INTEGER,
                user_id INTEGER,
                amount REAL,
                description TEXT,
                created_at TEXT
            )''')
            
            # Логи ошибок
            cursor.execute('''CREATE TABLE IF NOT EXISTS error_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                error_text TEXT,
                traceback TEXT,
                created_at TEXT
            )''')
            
            # Напоминания
            cursor.execute('''CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                chat_id INTEGER,
                text TEXT,
                remind_at TEXT,
                created_at TEXT
            )''')
            
            # Локации
            cursor.execute('''CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                latitude REAL,
                longitude REAL,
                place_name TEXT,
                created_at TEXT
            )''')
            
            # Чаты встреч
            cursor.execute('''CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meeting_id INTEGER,
                user_id INTEGER,
                message TEXT,
                created_at TEXT
            )''')
            
            # Опросы
            cursor.execute('''CREATE TABLE IF NOT EXISTS polls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meeting_id INTEGER,
                creator_id INTEGER,
                question TEXT,
                options TEXT,
                created_at TEXT
            )''')
            
            # Голоса в опросах
            cursor.execute('''CREATE TABLE IF NOT EXISTS poll_votes (
                poll_id INTEGER,
                user_id INTEGER,
                option_index INTEGER,
                PRIMARY KEY (poll_id, user_id)
            )''')
            
            # Чек-листы
            cursor.execute('''CREATE TABLE IF NOT EXISTS checklists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meeting_id INTEGER,
                user_id INTEGER,
                task TEXT,
                done INTEGER DEFAULT 0,
                created_at TEXT
            )''')
            
            conn.commit()
            logger.info("✅ База данных инициализирована")

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def execute(self, query: str, params: tuple = ()):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None

    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
