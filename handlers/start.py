from telebot import TeleBot
from dotenv import load_dotenv
from botconfig import BotConfig
from keyboards.botreplykeyboards import general_menu

load_dotenv()

TOKEN = BotConfig().token
bot = TeleBot(TOKEN)

def start_handler(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        chat_id = message.chat.id
        bot.send_message(chat_id, "Assalomu alaykum! Taqdimot bo'timizga xush kelibsiz. Bo'limlardan birini tanlang", reply_markup=general_menu())