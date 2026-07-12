"""Утилиты для красивого форматирования сообщений"""

def bold(text: str) -> str:
    return f"<b>{text}</b>"

def italic(text: str) -> str:
    return f"<i>{text}</i>"

def code(text: str) -> str:
    return f"<code>{text}</code>"

def pre(text: str) -> str:
    return f"<pre>{text}</pre>"

def link(text: str, url: str) -> str:
    return f'<a href="{url}">{text}</a>'

def spoiler(text: str) -> str:
    return f'<span class="tg-spoiler">{text}</span>'

def blockquote(text: str) -> str:
    return f"<blockquote>{text}</blockquote>"

def header(text: str, level: int = 1) -> str:
    return f"<b>{text}</b>" if level == 1 else f"<u>{text}</u>"

def divider() -> str:
    return "─" * 30

def emoji_icon(name: str) -> str:
    icons = {
        "weather": "🌤", "meeting": "📅", "profile": "👤",
        "friends": "👥", "expense": "💰", "reminder": "⏰",
        "calendar": "📆", "location": "📍", "stats": "📊",
        "backup": "💾", "help": "❓", "success": "✅",
        "error": "❌", "warning": "⚠️", "info": "ℹ️",
        "chat": "💬", "poll": "📊", "checklist": "📋",
        "notify": "📢", "folder": "📂", "idea": "💡",
        "plan": "📝", "start": "🚀", "settings": "⚙️",
        "search": "🔍", "pin": "📌", "time": "🕐",
        "date": "📅", "person": "🧑", "group": "👥",
        "money": "💵", "gift": "🎁", "star": "⭐",
        "fire": "🔥", "question": "❓", "exclamation": "❗",
        "thinking": "🤔", "wave": "👋", "robot": "🤖",
        "brain": "🧠", "sparkles": "✨", "check": "✔️",
        "cross": "❌", "plus": "➕", "minus": "➖",
        "arrow_right": "➡️", "arrow_left": "⬅️",
        "arrow_up": "⬆️", "arrow_down": "⬇️"
    }
    return icons.get(name, "•")
