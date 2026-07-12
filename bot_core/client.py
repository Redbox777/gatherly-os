import requests
import json
import time
from core import get_logger

logger = get_logger(__name__)

class TelegramClient:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.telegram.org/bot{}/".format(self.token)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Connection": "keep-alive"
        })

    def _request(self, method: str, params: dict = None, json_data: dict = None, retries: int = 3):
        url = self.base_url + method
        for attempt in range(retries):
            try:
                if json_data:
                    resp = self.session.post(url, json=json_data, timeout=20)
                else:
                    resp = self.session.get(url, params=params, timeout=20)

                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("ok"):
                        return data.get("result", {})
                else:
                    logger.warning(f"Ошибка {resp.status_code}, попытка {attempt+1}/{retries}")

            except requests.exceptions.Timeout:
                logger.warning(f"Таймаут, попытка {attempt+1}/{retries}")
            except requests.exceptions.ConnectionError:
                logger.warning(f"Ошибка соединения, попытка {attempt+1}/{retries}")
            except Exception as e:
                logger.error(f"Ошибка: {e}")

            time.sleep(2)

        return {}

    def get_updates(self, offset: int = None, timeout: int = 30):
        params = {"timeout": timeout}
        if offset:
            params["offset"] = offset
        result = self._request("getUpdates", params=params)
        return result if isinstance(result, list) else []

    def send_message(self, chat_id: int, text: str, keyboard: dict = None, parse_mode: str = None):
        data = {"chat_id": chat_id, "text": text}
        if keyboard:
            data["reply_markup"] = json.dumps(keyboard)
        if parse_mode:
            data["parse_mode"] = parse_mode
        return self._request("sendMessage", json_data=data)

    def edit_message(self, chat_id: int, message_id: int, text: str, keyboard: dict = None):
        data = {"chat_id": chat_id, "message_id": message_id, "text": text}
        if keyboard:
            data["reply_markup"] = json.dumps(keyboard)
        return self._request("editMessageText", json_data=data)

    def answer_callback(self, callback_id: str, text: str = None):
        data = {"callback_query_id": callback_id}
        if text:
            data["text"] = text
        return self._request("answerCallbackQuery", json_data=data)

    def delete_message(self, chat_id: int, message_id: int):
        data = {"chat_id": chat_id, "message_id": message_id}
        return self._request("deleteMessage", json_data=data)
