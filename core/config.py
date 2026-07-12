from dataclasses import dataclass

@dataclass
class BotConfig:
    token: str
    admin_id: int

@dataclass
class DatabaseConfig:
    path: str

@dataclass
class LoggingConfig:
    level: str
    max_size_mb: int
    backup_count: int

@dataclass
class AnalyticsConfig:
    enabled: bool
    report_time: str

@dataclass
class HealthConfig:
    enabled: bool
    check_interval_sec: int

@dataclass
class WeatherConfig:
    api: str

@dataclass
class Config:
    bot: BotConfig
    database: DatabaseConfig
    logging: LoggingConfig
    analytics: AnalyticsConfig
    health: HealthConfig
    weather: WeatherConfig

def load_config():
    try:
        from config import BOT_TOKEN, ADMIN_ID
        return Config(
            bot=BotConfig(token=BOT_TOKEN, admin_id=ADMIN_ID),
            database=DatabaseConfig(path="gatherly.db"),
            logging=LoggingConfig(level="INFO", max_size_mb=10, backup_count=5),
            analytics=AnalyticsConfig(enabled=True, report_time="23:59"),
            health=HealthConfig(enabled=True, check_interval_sec=60),
            weather=WeatherConfig(api="open-meteo")
        )
    except ImportError:
        print("❌ config.py не найден! Создай config.py с BOT_TOKEN")
        raise
