import calendar
from datetime import datetime

def generate_calendar(year: int, month: int, prefix: str = "cal"):
    """Генерирует inline-клавиатуру календаря"""
    now = datetime.now()
    if not year:
        year = now.year
    if not month:
        month = now.month

    cal = calendar.monthcalendar(year, month)
    keyboard = []

    # Заголовок
    month_name = calendar.month_name[month]
    keyboard.append([{
        "text": f"📅 {month_name} {year}",
        "callback_data": f"{prefix}_none"
    }])

    # Дни недели
    weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    keyboard.append([
        {"text": d, "callback_data": f"{prefix}_none"} for d in weekdays
    ])

    # Дни месяца
    for week in cal:
        row = []
        for day in week:
            if day == 0:
                row.append({"text": " ", "callback_data": f"{prefix}_none"})
            else:
                date_str = f"{year}-{month:02d}-{day:02d}"
                row.append({
                    "text": str(day),
                    "callback_data": f"{prefix}_{date_str}"
                })
        keyboard.append(row)

    # Навигация
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year = year - 1

    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year = year + 1

    keyboard.append([
        {"text": "◀", "callback_data": f"{prefix}_{prev_year}_{prev_month}"},
        {"text": "Сегодня", "callback_data": f"{prefix}_today"},
        {"text": "▶", "callback_data": f"{prefix}_{next_year}_{next_month}"}
    ])

    return {"inline_keyboard": keyboard}


def parse_callback(data: str):
    """Разбирает callback_data календаря"""
    parts = data.split("_")
    
    # Выбор даты: cal_2026-07-15
    if len(parts) == 2 and parts[0] == "cal" and "-" in parts[1]:
        return "date", parts[1]
    
    # Навигация: cal_2026_7
    if len(parts) == 3 and parts[0] == "cal":
        return "navigate", f"{parts[1]}_{parts[2]}"
    
    # Сегодня
    if data == "cal_today":
        now = datetime.now()
        return "date", now.strftime("%Y-%m-%d")
    
    return "none", ""
