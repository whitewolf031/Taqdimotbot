# handlers/profile.py
from telebot import types
from taqdimot_app.models import User  # Sizning model nomingiz

def my_handler(bot):
    @bot.message_handler(commands=['my'])
    def show_profile(message):
        chat_id = message.chat.id
        try:
            user = User.objects.get(chat_id=chat_id)
            username = f"@{user.username}" if user.username else "—"
            last_name = user.last_name or ""
            full_name = f"{user.first_name} {last_name}".strip()

            response = (
                f"👤 Sizning profilingiz:\n\n"
                f"ID: {user.chat_id}\n"
                f"Ism: {full_name}\n"
                f"Username: {username}"
            )
            bot.send_message(chat_id, response)
        except User.DoesNotExist:
            bot.send_message(chat_id, "❌ Siz hali ro'yxatdan o'tmagansiz!")