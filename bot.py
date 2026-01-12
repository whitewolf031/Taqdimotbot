from telebot import TeleBot
from handlers.start import start_handler
from handlers.contact import contact_handler
from botconfig import BotConfig

TOKEN = BotConfig().token
bot = TeleBot(TOKEN)

start_handler(bot)
contact_handler(bot)

bot.polling(non_stop=True)