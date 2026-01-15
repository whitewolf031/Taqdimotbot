from state.storage import user_state, user_info
from keyboards.botreplykeyboards import take_contact, general_menu
from utils import private_only
from botconfig import BotConfig
import re, time

group_id = BotConfig().group_id

@private_only
def admin_contact(bot, msg):
    chat_id = msg.chat.id
    bot.send_message(chat_id, "Ismingizni kiriting:")
    user_state[chat_id] = "take_phone"

@private_only
def take_phone(bot, msg):
    chat_id = msg.chat.id
    user_info.setdefault(chat_id, {})
    user_info[chat_id]["name"] = msg.text
    bot.send_message(chat_id, "Telefon raqamingizni kiriting:", reply_markup=take_contact())
    user_state[chat_id] = "user_message"

def is_valid_phone(phone: str) -> bool:
    pattern = r'^(?:\+998\d{9}|998\d{9}|\d{9})$'
    return bool(re.match(pattern, phone))

@private_only
def user_message(bot, msg):
    chat_id = msg.chat.id
    phone = msg.contact.phone_number if msg.content_type == "contact" else msg.text.strip()
    if not is_valid_phone(phone):
        bot.send_message(chat_id, "❌ Telefon raqami noto‘g‘ri formatda.")
        return
    user_info[chat_id]["phone"] = phone
    bot.send_message(chat_id, "Xabaringizni kiriting:")
    user_state[chat_id] = "commit_message"

@private_only
def commit_message(bot, msg):
    chat_id = msg.chat.id
    info = user_info.pop(chat_id)
    user_state.pop(chat_id, None)
    username = msg.from_user.username or "Noma’lum"

    bot.send_message(
        group_id,
        f"@{username}\n👤 {info['name']}\n📞 {info['phone']}\n✉️ {msg.text}"
    )

    time.sleep(1)
    bot.send_message(chat_id, "✅ Xabar jo‘natildi", reply_markup=general_menu())