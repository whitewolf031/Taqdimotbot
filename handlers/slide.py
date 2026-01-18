from telebot import TeleBot
from dotenv import load_dotenv
from botconfig import BotConfig
from utils import *

load_dotenv()

TOKEN = BotConfig().token
bot = TeleBot(TOKEN)


def slide_handler(bot):
    @bot.message_handler(commands=['slide'])

    def send_slide(message):
        text = (
            "📊 *Slayd bo‘limi*\n\n"
            "Hozircha slayd avtomatik tayyorlash funksiyasi "
            "ishlab chiqilmoqda 🚧\n\n"
            "🔜 Tez orada siz:\n"
            "• Slayd mavzusini kiritasiz\n"
            "• Slayd sonini tanlaysiz\n"
            "• PowerPoint (.pptx) fayl olasiz\n\n"
            "Iltimos, biroz kuting 🙂"
        )

        bot.send_message(
            chat_id=message.chat.id,
            text=text,
            parse_mode="Markdown"
        )
