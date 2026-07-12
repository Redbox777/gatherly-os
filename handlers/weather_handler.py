from bot_core.client import TelegramClient
from services import WeatherService
from bot_core.keyboards import weather_menu, back_menu

class WeatherHandler:
    def __init__(self, client: TelegramClient):
        self.client = client
        self.weather_service = WeatherService()

    def handle(self, chat_id: int, city_name: str):
        """Обработчик погоды"""
        self.client.send_message(chat_id, f"🔍 Ищу погоду для {city_name}...")
        result = self.weather_service.get_weather(city_name)
        
        if "error" in result:
            self.client.send_message(chat_id, result["error"], back_menu())
        else:
            self.client.send_message(chat_id, result["text"], weather_menu())

    def show_menu(self, chat_id: int):
        """Показать меню погоды"""
        self.client.send_message(chat_id, "🌤 Выбери действие:", weather_menu())
