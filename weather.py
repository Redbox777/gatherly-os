import requests

def get_coordinates(city_name):
    """Получает координаты по названию города через Open-Meteo Geocoding"""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ru&format=json"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get("results"):
            result = data["results"][0]
            return {
                "name": result["name"],
                "country": result.get("country", ""),
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "timezone": result.get("timezone", "auto")
            }
        return None
    except Exception as e:
        print(f"Ошибка геокодинга: {e}")
        return None

def get_weather(lat, lon, timezone="auto"):
    """Получает текущую погоду через Open-Meteo"""
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&"
        f"daily=sunrise,sunset&"
        f"timezone={timezone}&"
        f"forecast_days=1"
    )
    try:
        resp = requests.get(url, timeout=10)
        return resp.json()
    except Exception as e:
        print(f"Ошибка погоды: {e}")
        return None

def get_weather_emoji(code):
    """Переводит код погоды Open-Meteo в эмодзи"""
    weather_codes = {
        0: "☀️", 1: "🌤", 2: "⛅", 3: "☁️",
        45: "🌫", 48: "🌫",
        51: "🌧", 53: "🌧", 55: "🌧",
        61: "🌧", 63: "🌧", 65: "🌧",
        71: "❄️", 73: "❄️", 75: "❄️",
        80: "🌦", 81: "🌦", 82: "🌧",
        95: "⛈", 96: "⛈", 99: "⛈"
    }
    return weather_codes.get(code, "🌈")

def format_weather(city_name, weather_data, geodata):
    """Форматирует погоду для отправки пользователю"""
    current = weather_data.get("current", {})
    daily = weather_data.get("daily", {})
    
    temp = current.get("temperature_2m", "?")
    humidity = current.get("relative_humidity_2m", "?")
    wind = current.get("wind_speed_10m", "?")
    code = current.get("weather_code", 0)
    emoji = get_weather_emoji(code)
    
    sunrise = daily.get("sunrise", ["?"])[0] if daily.get("sunrise") else "?"
    sunset = daily.get("sunset", ["?"])[0] if daily.get("sunset") else "?"
    
    sunrise_time = sunrise.split("T")[1][:5] if "T" in sunrise else sunrise
    sunset_time = sunset.split("T")[1][:5] if "T" in sunset else sunset
    
    country = geodata.get("country", "")
    name = geodata.get("name", city_name)
    location = f"{name}, {country}" if country else name
    
    text = (
        f"📍 {location}\n"
        f"{emoji} {temp}°C\n"
        f"💨 Ветер {wind} км/ч · 💧 {humidity}%\n"
        f"🌅 Восход: {sunrise_time}\n"
        f"🌇 Закат: {sunset_time}"
    )
    return text
