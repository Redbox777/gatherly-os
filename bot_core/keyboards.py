def main_menu():
    return {
        "keyboard": [
            ["🌤 Погода", "📅 Создать встречу"],
            ["📋 Мои встречи", "👤 Профиль"],
            ["👥 Друзья", "⏰ Напоминания"],
            ["📅 Календарь", "📍 Геолокация"],
            ["📊 Статистика", "💾 Бэкап"],
            ["❓ Помощь"]
        ],
        "resize_keyboard": True
    }

def weather_menu():
    return {
        "keyboard": [
            ["🌍 Другой город"],
            ["🔙 Назад"]
        ],
        "resize_keyboard": True
    }

def back_menu():
    return {
        "keyboard": [["🔙 Назад"]],
        "resize_keyboard": True
    }

def location_keyboard():
    return {
        "keyboard": [
            [{"text": "📍 Отправить местоположение", "request_location": True}],
            ["🔙 Назад"]
        ],
        "resize_keyboard": True
    }
