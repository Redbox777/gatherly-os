import requests

TOKEN = "8998508373:AAEBs57cSLf236ndaal4zZ_6h_ht8WAZ6Sg"

url = f"https://api.telegram.org/bot{TOKEN}/getMe"

try:
    r = requests.get(url, timeout=10)
    print("Статус ответа:", r.status_code)
    print("Ответ:", r.json())
except Exception as e:
    print("Ошибка:", e)
