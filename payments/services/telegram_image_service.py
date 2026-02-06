import base64
import requests
from botconfig import BotConfig
from telebot import TeleBot

bot = TeleBot(BotConfig().token)

def download_telegram_photo_as_base64(file_id: str) -> str:
    file_info = bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{BotConfig().token}/{file_info.file_path}"

    response = requests.get(file_url)
    response.raise_for_status()

    return base64.b64encode(response.content).decode("utf-8")