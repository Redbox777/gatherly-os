from bot_core.client import TelegramClient
from services import MeetingService
from core import Database
from bot_core.keyboards import main_menu, back_menu

class MeetingHandler:
    def __init__(self, client: TelegramClient, db: Database):
        self.client = client
        self.meeting_service = MeetingService(db)
        self.states = {}

    def new_meeting(self, chat_id: int):
        """Начать создание встречи"""
        self.client.send_message(chat_id, "📝 Введите название встречи:", back_menu())
        self.states[chat_id] = {"step": "title"}

    def list_meetings(self, chat_id: int):
        """Показать список встреч"""
        meetings = self.meeting_service.get_user_meetings(chat_id)
        
        if not meetings:
            self.client.send_message(chat_id, "📭 У вас пока нет встреч.", main_menu())
            return
        
        text = "📋 **Ваши встречи:**\n\n"
        for m in meetings:
            text += f"#{m['id']} **{m['title']}**\n"
            text += f"📅 {m['date']} 🕐 {m['time']}\n"
            text += f"✅ {m['going']} | ❌ {m['not_going']} | 🤔 {m['maybe']}\n\n"
            if len(text) > 3000:
                self.client.send_message(chat_id, text, main_menu())
                text = ""
        
        if text:
            self.client.send_message(chat_id, text, main_menu())

    def show_meeting(self, chat_id: int, meeting_id: int):
        """Показать детали встречи"""
        meeting = self.meeting_service.get_meeting(meeting_id)
        if "error" in meeting:
            self.client.send_message(chat_id, meeting["error"], main_menu())
            return
        
        going = ', '.join([str(u) for u in meeting['going']]) or "—"
        not_going = ', '.join([str(u) for u in meeting['not_going']]) or "—"
        maybe = ', '.join([str(u) for u in meeting['maybe']]) or "—"
        
        text = (
            f"📌 **{meeting['title']}**\n"
            f"📅 Дата: {meeting['date']}\n"
            f"🕐 Время: {meeting['time']}\n"
            f"📍 Место: {meeting['place']}\n"
            f"📝 Описание: {meeting['description']}\n\n"
            f"✅ Идут ({len(meeting['going'])}): {going}\n"
            f"❌ Не идут ({len(meeting['not_going'])}): {not_going}\n"
            f"🤔 Может быть ({len(meeting['maybe'])}): {maybe}"
        )
        
        self.client.send_message(chat_id, text, main_menu())

    def vote(self, chat_id: int, meeting_id: int, status: str):
        """Голосование за встречу"""
        if self.meeting_service.vote(meeting_id, chat_id, status):
            self.client.send_message(chat_id, f"✅ Ваш голос принят!", main_menu())
            self.show_meeting(chat_id, meeting_id)
        else:
            self.client.send_message(chat_id, "❌ Ошибка голосования.", main_menu())

    def process_state(self, chat_id: int, text: str):
        """Обработка пошагового создания встречи"""
        state = self.states.get(chat_id)
        if not state:
            return
        
        step = state.get("step")
        
        # Если пользователь нажал "Назад" — отменяем создание
        if text == "🔙 Назад":
            del self.states[chat_id]
            self.client.send_message(chat_id, "❌ Создание встречи отменено.", main_menu())
            return
        
        if step == "title":
            state["title"] = text
            state["step"] = "date"
            self.client.send_message(chat_id, "📅 Введите дату (например: 2026-07-15):", back_menu())
        
        elif step == "date":
            state["date"] = text
            state["step"] = "time"
            self.client.send_message(chat_id, "🕐 Введите время (например: 18:30):", back_menu())
        
        elif step == "time":
            state["time"] = text
            state["step"] = "place"
            self.client.send_message(chat_id, "📍 Введите место встречи:", back_menu())
        
        elif step == "place":
            state["place"] = text
            state["step"] = "description"
            self.client.send_message(chat_id, "📝 Введите описание (или '-' чтобы пропустить):", back_menu())
        
        elif step == "description":
            if text == "-":
                text = None
            state["description"] = text
            
            # Создаём встречу
            meeting_id = self.meeting_service.create_meeting(
                creator_id=chat_id,
                title=state["title"],
                date=state["date"],
                time=state["time"],
                place=state["place"],
                description=state.get("description")
            )
            
            self.client.send_message(chat_id, f"✅ Встреча '{state['title']}' создана! ID: {meeting_id}", main_menu())
            self.show_meeting(chat_id, meeting_id)
            
            # Очищаем состояние
            del self.states[chat_id]
