from telebot import TeleBot
from dotenv import load_dotenv
from botconfig import BotConfig
from keyboards.botreplykeyboards import general_menu
from taqdimot_app.models import User
from utils import *

load_dotenv()

TOKEN = BotConfig().token
bot = TeleBot(TOKEN)


def start_handler(bot):
    @bot.message_handler(commands=['start'])
    @private_only
    def start(message):
        chat_id = message.chat.id

        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name

        # 🔹 User ni DB ga saqlash yoki yangilash
        user, created = User.objects.get_or_create(
            chat_id=chat_id,
            defaults={
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            }
        )

        # Agar user oldindan bor bo‘lsa, ma’lumotlarni yangilaymiz
        if not created:
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save(update_fields=["username", "first_name", "last_name"])

        bot.send_message(
            chat_id,
            "Assalomu alaykum! Taqdimot botimizga xush kelibsiz.\nBo‘limlardan birini tanlang.",
            reply_markup=general_menu()
        )
