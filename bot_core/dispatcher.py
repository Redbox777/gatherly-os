import time
from datetime import datetime
from core import Database, get_logger
from .client import TelegramClient
from .keyboards import main_menu, weather_menu, back_menu, location_keyboard
from handlers import (
    StartHandler,
    WeatherHandler,
    ProfileHandler,
    MeetingHandler,
    FriendHandler,
    ExpenseHandler,
    ReminderHandler,
    StatsHandler,
    BackupHandler,
    ChatHandler,
    PollHandler,
    ChecklistHandler,
    NotificationHandler
)
from bot_core.calendar import generate_calendar, parse_callback
from analytics import ErrorCollector, ReportGenerator

logger = get_logger(__name__)

MENU_COMMANDS = [
    "🌤 Погода", "📅 Создать встречу", "📋 Мои встречи", "👤 Профиль",
    "👥 Друзья", "⏰ Напоминания", "📆 Календарь", "📍 Геолокация",
    "📊 Статистика", "💾 Бэкап", "📊 Ошибки", "📋 Отчёт",
    "❓ Помощь", "🔙 Назад", "🌍 Другой город", "✏️ Редактировать профиль",
    "🏙 Город", "🎯 Интересы", "📨 Заявки"
]

class Dispatcher:
    def __init__(self, client: TelegramClient, db: Database):
        self.client = client
        self.db = db
        
        self.start_handler = StartHandler(client, db)
        self.weather_handler = WeatherHandler(client)
        self.profile_handler = ProfileHandler(client, db)
        self.meeting_handler = MeetingHandler(client, db)
        self.friend_handler = FriendHandler(client, db)
        self.expense_handler = ExpenseHandler(client, db)
        self.reminder_handler = ReminderHandler(client, db)
        self.stats_handler = StatsHandler(client, db)
        self.backup_handler = BackupHandler(client, db)
        self.chat_handler = ChatHandler(client, db)
        self.poll_handler = PollHandler(client, db)
        self.checklist_handler = ChecklistHandler(client, db)
        self.notification_handler = NotificationHandler(client, db)
        self.error_collector = ErrorCollector()

    def process_update(self, update: dict):
        if "callback_query" in update:
            self._handle_callback(update["callback_query"])
            return

        if "message" not in update:
            return

        msg = update["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "")
        first_name = msg["from"]["first_name"]
        username = msg["from"].get("username", "")

        logger.info(f"{first_name} ({chat_id}): {text}")

        if "location" in msg:
            lat = msg["location"]["latitude"]
            lon = msg["location"]["longitude"]
            self.client.send_message(
                chat_id,
                f"📍 Получены координаты:\nШирота: {lat}\nДолгота: {lon}\n\nСсылка: https://maps.google.com/?q={lat},{lon}",
                main_menu()
            )
            return

        if chat_id in self.profile_handler.states:
            self.profile_handler.process_state(chat_id, text)
            return
        
        if chat_id in self.meeting_handler.states:
            self.meeting_handler.process_state(chat_id, text)
            return
        
        if chat_id in self.expense_handler.states:
            self.expense_handler.process_state(chat_id, text)
            return

        if text == "/start":
            self.start_handler.handle(chat_id, first_name, username)
        
        elif text == "🌤 Погода":
            self.weather_handler.show_menu(chat_id)
        elif text == "🌍 Другой город":
            self.client.send_message(chat_id, "🏙 Введите название города:", back_menu())
            self.profile_handler.states[chat_id] = "waiting_weather"
        elif text.startswith("/weather"):
            city = text.replace("/weather", "").strip()
            if city:
                self.weather_handler.handle(chat_id, city)
            else:
                self.client.send_message(chat_id, "📝 Пример: /weather Орел")
        
        elif text == "👤 Профиль":
            self.profile_handler.show_profile(chat_id)
        elif text == "✏️ Редактировать профиль":
            self.client.send_message(chat_id, "📝 Что хотите изменить?", {
                "keyboard": [
                    ["🏙 Город", "🎯 Интересы"],
                    ["🔙 Назад"]
                ],
                "resize_keyboard": True
            })
        elif text == "🏙 Город":
            self.profile_handler.edit_city(chat_id)
        elif text == "🎯 Интересы":
            self.profile_handler.edit_interests(chat_id)
        
        elif text == "📅 Создать встречу":
            self.meeting_handler.new_meeting(chat_id)
        elif text == "📋 Мои встречи":
            self.meeting_handler.list_meetings(chat_id)
        elif text.startswith("/meeting"):
            parts = text.split()
            if len(parts) >= 2:
                try:
                    meeting_id = int(parts[1])
                    self.meeting_handler.show_meeting(chat_id, meeting_id)
                except ValueError:
                    self.client.send_message(chat_id, "❌ Введите корректный ID встречи.")
            else:
                self.client.send_message(chat_id, "📝 Пример: /meeting 1")
        elif text.startswith("/vote"):
            parts = text.split()
            if len(parts) >= 3:
                try:
                    meeting_id = int(parts[1])
                    status = parts[2]
                    self.meeting_handler.vote(chat_id, meeting_id, status)
                except ValueError:
                    self.client.send_message(chat_id, "❌ Пример: /vote 1 going")
            else:
                self.client.send_message(chat_id, "❌ Пример: /vote 1 going")
        
        elif text == "👥 Друзья":
            self.friend_handler.list_friends(chat_id)
        elif text.startswith("/addme"):
            parts = text.split()
            if len(parts) >= 2:
                self.friend_handler.add_friend(chat_id, parts[1])
            else:
                self.client.send_message(chat_id, "❌ Введите ID друга: /addme 123456789")
        elif text == "📨 Заявки":
            self.friend_handler.list_requests(chat_id)
        elif text.startswith("/accept"):
            parts = text.split()
            if len(parts) >= 2:
                self.friend_handler.accept_request(chat_id, parts[1])
            else:
                self.client.send_message(chat_id, "❌ Пример: /accept 123456789")
        elif text.startswith("/reject"):
            parts = text.split()
            if len(parts) >= 2:
                self.friend_handler.reject_request(chat_id, parts[1])
            else:
                self.client.send_message(chat_id, "❌ Пример: /reject 123456789")
        
        elif text.startswith("/expense"):
            parts = text.split()
            if len(parts) >= 2:
                self.expense_handler.add_expense(chat_id, parts[1])
            else:
                self.client.send_message(chat_id, "❌ Пример: /expense 1")
        elif text.startswith("/expenses"):
            parts = text.split()
            if len(parts) >= 2:
                self.expense_handler.list_expenses(chat_id, parts[1])
            else:
                self.client.send_message(chat_id, "❌ Пример: /expenses 1")
        
        elif text == "⏰ Напоминания":
            self.client.send_message(chat_id, "⏰ Напоминания:\n/remind — создать\n/reminders — список\n/delremind — удалить", main_menu())
        elif text.startswith("/remind"):
            self.reminder_handler.schedule(chat_id, text)
        elif text == "/reminders":
            self.reminder_handler.list_reminders(chat_id)
        elif text.startswith("/delremind"):
            parts = text.split()
            if len(parts) >= 2:
                self.reminder_handler.delete(chat_id, parts[1])
            else:
                self.client.send_message(chat_id, "❌ Пример: /delremind 1", main_menu())
        
        elif text == "/calendar" or text == "📆 Календарь":
            now = datetime.now()
            keyboard = generate_calendar(now.year, now.month)
            self.client.send_message(chat_id, "📅 Выберите дату:", keyboard=keyboard)
        
        elif text == "📍 Геолокация":
            self.client.send_message(chat_id, "📍 Отправьте своё местоположение:", keyboard=location_keyboard())
        
        elif text == "📊 Статистика":
            self.stats_handler.show_user_stats(chat_id)
        
        elif text == "💾 Бэкап":
            self.backup_handler.create_backup(chat_id)
        
        elif text == "/adminstats":
            self.stats_handler.show_global_stats(chat_id)
        
        elif text == "/backups":
            self.backup_handler.list_backups(chat_id)
        
        # === АНАЛИТИКА ОШИБОК ===
        elif text == "📊 Ошибки" or text == "/errors":
            try:
                errors = self.error_collector.get_errors(limit=20, resolved=0)
                if not errors:
                    self.client.send_message(chat_id, "✅ Неисправленных ошибок нет!", main_menu())
                    return
                
                text_msg = f"📊 **Ошибки ({len(errors)} неисправлено):**\n\n"
                for e in errors[:10]:
                    text_msg += f"#{e['id']} {e['timestamp'][:16]} | {e['error_type']}\n"
                    text_msg += f"  {e['error_message'][:60]}...\n\n"
                
                text_msg += f"\n/resolve <ID> — отметить как исправленное"
                self.client.send_message(chat_id, text_msg, main_menu(), parse_mode="Markdown")
            except Exception as e:
                self.error_collector.add_error(e, chat_id, "/errors")
                self.client.send_message(chat_id, "❌ Ошибка при получении списка ошибок.", main_menu())
        
        elif text.startswith("/resolve"):
            parts = text.split()
            if len(parts) >= 2:
                try:
                    error_id = int(parts[1])
                    self.error_collector.mark_resolved(error_id)
                    self.client.send_message(chat_id, f"✅ Ошибка #{error_id} отмечена как исправленная!", main_menu())
                except ValueError:
                    self.client.send_message(chat_id, "❌ Введите корректный ID ошибки.", main_menu())
                except Exception as e:
                    self.error_collector.add_error(e, chat_id, f"/resolve {parts[1] if len(parts)>1 else ''}")
                    self.client.send_message(chat_id, "❌ Ошибка при отметке.", main_menu())
            else:
                self.client.send_message(chat_id, "❌ Пример: /resolve 1", main_menu())
        
        elif text == "📋 Отчёт" or text == "/sendreport":
            try:
                from analytics import DailyReport
                admin_id = self.config.bot.admin_id
                daily = DailyReport(self.client, admin_id)
                daily.send_report()
                self.client.send_message(chat_id, "✅ Отчёт отправлен!", main_menu())
            except Exception as e:
                self.error_collector.add_error(e, chat_id, "/sendreport")
                self.client.send_message(chat_id, "❌ Ошибка при отправке отчёта.", main_menu())
        
        # === ЧАТ ===
        elif text.startswith("/chat"):
            parts = text.split()
            if len(parts) >= 2:
                self.chat_handler.enter_chat(chat_id, parts[1])
            else:
                self.client.send_message(chat_id, "❌ Пример: /chat 1", main_menu())

        elif text.startswith("/sendchat"):
            parts = text.split(maxsplit=2)
            if len(parts) >= 3:
                self.chat_handler.send_chat_message(chat_id, parts[1], parts[2])
            else:
                self.client.send_message(chat_id, "❌ Пример: /sendchat 1 Текст", main_menu())

        elif text.startswith("/chathistory"):
            parts = text.split()
            if len(parts) >= 2:
                self.chat_handler.get_chat_history(chat_id, parts[1])
            else:
                self.client.send_message(chat_id, "❌ Пример: /chathistory 1", main_menu())

        # === ОПРОСЫ ===
        elif text.startswith("/poll"):
            self.poll_handler.create_poll(chat_id, text)

        # === ЧЕК-ЛИСТЫ ===
        elif text.startswith("/checklist"):
            parts = text.split()
            if len(parts) >= 2:
                self.checklist_handler.create_checklist(chat_id, parts[1])
            else:
                self.client.send_message(chat_id, "❌ Пример: /checklist 1", main_menu())

        elif text.startswith("/done"):
            parts = text.split()
            if len(parts) >= 2:
                self.checklist_handler.toggle_done(chat_id, parts[1])
            else:
                self.client.send_message(chat_id, "❌ Пример: /done 1", main_menu())

        elif text.startswith("/delete"):
            parts = text.split()
            if len(parts) >= 2:
                self.checklist_handler.delete_task(chat_id, parts[1])
            else:
                self.client.send_message(chat_id, "❌ Пример: /delete 1", main_menu())

        # === УВЕДОМЛЕНИЯ ===
        elif text.startswith("/notify"):
            self.notification_handler.notify_all(chat_id, text)
        
        elif text == "❓ Помощь":
            self._show_help(chat_id)
        
        elif text == "🔙 Назад":
            self.start_handler.handle(chat_id, first_name, username)
        
        elif text and not text.startswith("/") and text not in MENU_COMMANDS:
            self.weather_handler.handle(chat_id, text)
        
        else:
            self.client.send_message(chat_id, "📩 Используйте /start для меню.", main_menu())

    def _show_help(self, chat_id: int):
        text = """📋 **ПОМОЩЬ ПО БОТУ**

👤 **Профиль**
/profile — показать профиль

🌤 **Погода**
/weather <город> — погода

📅 **Встречи**
/new — создать встречу
/meetings — мои встречи
/meeting <ID> — детали встречи
/vote <ID> going/not_going/maybe — голосовать

👥 **Друзья**
/friends — список друзей
/addme <ID> — добавить друга
/requests — входящие заявки

💰 **Расходы**
/expense <ID> — добавить расход
/expenses <ID> — список расходов

⏰ **Напоминания**
/remind 2026-07-12T18:00 Текст — создать
/reminders — мои напоминания
/delremind <ID> — удалить

📆 **Календарь**
/calendar — выбрать дату

📍 **Геолокация**
/location — отправить местоположение

📊 **Статистика**
/stats — моя статистика

💾 **Бэкап**
/backup — создать бэкап
/backups — список бэкапов

💬 **Чат встречи**
/chat <ID> — войти в чат
/sendchat <ID> <текст> — отправить сообщение
/chathistory <ID> — история чата

📊 **Опросы**
/poll <ID> <вопрос> <вариант1,вариант2,...> — создать опрос

📋 **Чек-листы**
/checklist <ID> — создать чек-лист
/done <ID> — отметить задачу
/delete <ID> — удалить задачу

📢 **Уведомления**
/notify <ID> <текст> — уведомить всех участников

📊 **Аналитика ошибок**
/errors — список ошибок
/resolve <ID> — отметить исправленную
/sendreport — отправить отчёт"""
        self.client.send_message(chat_id, text, main_menu(), parse_mode="Markdown")

    def _handle_callback(self, callback: dict):
        data = callback.get("data", "")
        chat_id = callback["from"]["id"]
        message_id = callback["message"]["message_id"]
        
        if data.startswith("cal_"):
            action, value = parse_callback(data)
            if action == "date":
                self.client.send_message(chat_id, f"✅ Выбрана дата: {value}", main_menu())
                self.client.answer_callback(callback["id"])
            elif action == "navigate":
                year, month = map(int, value.split("_"))
                keyboard = generate_calendar(year, month)
                self.client.edit_message(chat_id, message_id, "📅 Выберите дату:", keyboard=keyboard)
                self.client.answer_callback(callback["id"])
            else:
                self.client.answer_callback(callback["id"])
            return
        
        elif data.startswith("poll_"):
            parts = data.split("_")
            poll_id = int(parts[1])
            option_index = int(parts[2])
            from services import PollService
            poll_service = PollService(self.db)
            if poll_service.vote(poll_id, chat_id, option_index):
                self.client.send_message(chat_id, f"✅ Ваш голос принят!", main_menu())
            else:
                self.client.send_message(chat_id, f"❌ Ошибка голосования.", main_menu())
            self.client.answer_callback(callback["id"])
            return
        
        self.client.answer_callback(callback["id"])
        self.client.send_message(chat_id, "🛠 Функция в разработке.", main_menu())
