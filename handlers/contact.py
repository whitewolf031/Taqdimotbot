from keyboards.botreplykeyboards import take_contact, general_menu
import time
import re
from utils import *
from dotenv import load_dotenv
from keyboards.botreplykeyboards import general_menu
from botconfig import BotConfig

load_dotenv()

group_id = BotConfig().group_id

user_info = {}
user_state = {}

def contact_handler(bot):
    # @bot.message_handler(func=lambda message: True, content_types=['text', 'contact'])
    @private_only
    def state_manager(msg):
        chat_id = msg.chat.id
        # Agar yangi user bo‘lsa, default qilib main_menu qilamiz
        state = user_state.get(chat_id, "main_menu")

        if msg.text == "Bog'lanish":
            admin_contact(msg)

        if state == "take_phone":
            take_phone(msg)

        elif state == "user_message":
            user_message(msg)

        elif state == "commit_message":
            commit_message(msg)

    @private_only
    def admin_contact(msg):
        chat_id = msg.chat.id
        bot.send_message(chat_id, "Ismingizni kiriting: ")
        user_state[chat_id] = "take_phone"

    @private_only
    def take_phone(msg):
        chat_id = msg.chat.id
        user_info.setdefault(chat_id, {})
        user_info[chat_id]["name"] = msg.text
        bot.send_message(chat_id, "Telefon raqamingizni kiriting: ", reply_markup=take_contact())
        user_state[chat_id] = "user_message"

    @private_only
    def is_valid_phone(phone: str) -> bool:
        # ✅ faqat 998 bilan boshlanishi yoki +998 bilan boshlanishiga ruxsat
        pattern = r'^(?:\+998\d{9}|998\d{9}|\d{9})$'
        return bool(re.match(pattern, phone))

    @private_only
    def user_message(msg):
        chat_id = msg.chat.id

        if msg.content_type == "contact":
            phone = msg.contact.phone_number
        else:
            phone = msg.text.strip()

        if not is_valid_phone(phone):
            bot.send_message(
                chat_id,
                "❌ Telefon raqami noto‘g‘ri.\nIltimos, +998901234567 formatida kiriting."
            )
            return

        user_info.setdefault(chat_id, {})
        user_info[chat_id]["phone"] = phone

        bot.send_message(chat_id, "Xabaringizni kiriting: ")
        user_state[chat_id] = "commit_message"

    @private_only
    def commit_message(msg):
        chat_id = msg.chat.id
        user_info.setdefault(chat_id, {})
        user_info[chat_id]["xabar"] = msg.text

        info = user_info.get(chat_id, {})
        username = msg.from_user.username or "Noma’lum"

        bot.send_message(
            group_id,
            f"Username: @{username}\n"
            f"👤 {info.get('name')}\n"
            f"📞 {info.get('phone')}\n"
            f"✉️ {info.get('xabar')}"
        )

        time.sleep(2)
        bot.send_message(chat_id, "Xabaringiz jo'natildi. Menu ga qaytingiz", reply_markup=general_menu())