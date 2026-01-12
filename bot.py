from telebot import TeleBot
from handlers.start import start_handler
from handlers.contact import contact_handler
from handlers.balans import balance_handler
from botconfig import BotConfig

def start_bot():
    bot = TeleBot(BotConfig().token)

    start_handler(bot)
    contact_handler(bot)
    balance_handler(bot)

    print("Telegram bot ishga tushdi...")
    bot.infinity_polling(skip_pending=True)