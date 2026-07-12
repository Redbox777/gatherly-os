import sys
import os

# Добавляем корневую папку в путь, чтобы найти weather.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather import get_coordinates, get_weather, format_weather
from core import get_logger

logger = get_logger(__name__)

class WeatherService:
    def get_weather(self, city_name: str) -> dict:
        try:
            geo = get_coordinates(city_name)
            if not geo:
                return {"error": f"❌ Город '{city_name}' не найден."}
            
            weather = get_weather(
                geo["latitude"],
                geo["longitude"],
                geo.get("timezone", "auto")
            )
            
            if not weather:
                return {"error": "❌ Не удалось получить погоду."}
            
            text = format_weather(city_name, weather, geo)
            return {"text": text}
        except Exception as e:
            logger.error(f"Ошибка погоды: {e}")
            return {"error": "❌ Ошибка получения погоды."}
