#!/usr/bin/env python3
"""
Gatherly OS — главный файл
"""

import sys
import time
import signal
from pathlib import Path

# Добавляем текущую папку в путь
sys.path.insert(0, str(Path(__file__).parent))

from core import load_config, setup_logging, get_logger, Database
from bot_core import Bot

logger = get_logger(__name__)

def signal_handler(sig, frame):
    logger.info("👋 Получен сигнал остановки")
    sys.exit(0)

def main():
    # Загрузка конфигурации
    config = load_config()
    
    # Настройка логирования
    setup_logging(config)
    
    logger.info("🚀 Gatherly OS запущена")
    logger.info(f"📁 База данных: {config.database.path}")
    
    # Инициализация БД
    db = Database(config)
    
    # Инициализация Telegram бота
    bot = Bot(config)
    
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("👋 Остановка бота")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
