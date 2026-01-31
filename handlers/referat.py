from state.storage import user_state, user_data
from utils import private_only
from keyboards.botinlinekeyboards import referat_button, check_button, choose_languange
from keyboards.botreplykeyboards import betlar_soni, general_menu
from openai import OpenAI
import os
import requests
from django.conf import settings
from taqdimot_app.models import User
from payments.models import Payment, WorkUsage
from django.db.models import Sum
from decimal import Decimal
from taqdimot_app.services import balance_service
import time

client = OpenAI(api_key=settings.OPENAI_API_KEY)

REQUIRED_AMOUNT = Decimal("4000")

@private_only
def start_referat(bot, msg):
    chat_id = msg.chat.id

    user_state[chat_id] = 'referat_topic'
    user_data[chat_id] = {}

    bot.send_message(chat_id, "Mavzuni to'liq, bexato va tushunarli qilib kiriting.")

@private_only
def referat_topic(bot, msg):
    chat_id = msg.chat.id

    user_data[chat_id]["topic"] = msg.text
    user_state[chat_id] = "referat_institute"

    institut = ("Institut va kafedrangizni(majburiy emas) to'liq kiriting.\n\n"
            "Misol: <b>O‘ZBEKISTON RESPUBLIKASI OLIY TA’LIM FAN VA INNOVATSIYA VAZIRLIGI"
                        "SARBON UNIVERSITETI"
                        "AXBOROT XAVFSIZLIGI KAFEDRASI.</b>")

    bot.send_message(
        chat_id,
        institut,
        parse_mode="HTML"
    )

@private_only
def referat_institute(bot, msg):
    chat_id = msg.chat.id

    user_data[chat_id]["institute"] = msg.text
    user_state[chat_id] = "referat_author"

    mualif = ("Muallif ism-familiyasi, guruhi va kursini to'liq kiriting.\n\n"
            "📋Namuna: <b>Isroilov Ismoiljon Muhiddin o'g'li, 4-kurs, 21.36-guruh.</b>")

    bot.send_message(
        chat_id,
        mualif,
        parse_mode="HTML"
    )

@private_only
def referat_author(bot, msg):
    chat_id = msg.chat.id

    user_data[chat_id]["author"] = msg.text
    user_state[chat_id] = "referat_type"

    bot.send_message(
        chat_id,
        "📄 Ish turini tanlang:",
        reply_markup=referat_button()
    )

@private_only
def referat_type(bot, call):
    chat_id = call.message.chat.id
    user_data[chat_id]["type"] = call.data
    user_state[chat_id] = "referat_bet"

    bot.send_message(chat_id, "Varaqlar sonini tanlang", reply_markup=betlar_soni())

@private_only
def referat_bet(bot, msg):
    chat_id = msg.chat.id
    user_data[chat_id]["bet"] = msg.text
    type = user_data[chat_id]["type"]
    user_state[chat_id] = "referat_languange"

    bot.send_message(chat_id, f"{type} ni tilini tanlang.", reply_markup=choose_languange())

@private_only
def referat_languange(bot, call):
    chat_id = call.message.chat.id
    user_data[chat_id]["til"] = call.data
    user_state[chat_id] = "choose_button"

    data = user_data[chat_id]

    text = (f"🌟 Ajoyib, quyidagi ma’lumotlarni tekshiring.\n\n"
        f"<b>{data["type"].upper()}</b>\n"
        f"<b>Mavzu: {data["topic"]}</b>\n"
        f"<b>Institut va kafedra:</b> {data['institute']}\n"
        f"<b>Muallif:</b> {data['author']}\n"
        f"<b>Sahifalar soni:</b> {data["bet"]}\n"
        f"<b>Tili:</b> {data["til"]}\n"
        f"<b>Hajmi:</b> {data['bet']} bet\n\n"
        f"<b>✅ Tayyorlash</b>\n"
        f"<b>✏️ O‘zgartirish</b>\n"
        "<b>🚫 Rad etish</b>")

    bot.send_message(chat_id, text, reply_markup=check_button(), parse_mode="HTML")

@private_only
def choose_button(bot, call):
    chat_id = call.message.chat.id
    data = user_data[chat_id]

    if call.data == "do":

        # 1️⃣ User
        user, _ = User.objects.get_or_create(
            chat_id=chat_id,
            defaults={
                "first_name": call.message.chat.first_name or "",
                "last_name": call.message.chat.last_name,
                "username": call.message.chat.username,
            }
        )

        # 2️⃣ Balansni tekshiramiz
        balance = balance_service.get_user_balance(user)

        if balance < REQUIRED_AMOUNT:
            bot.send_message(
                chat_id,
                f"❌ Hisobingizda mablag‘ yetarli emas.\n\n"
                f"💰 Balansingiz: {int(balance)} so‘m\n"
                f"📌 Kerakli summa: {int(REQUIRED_AMOUNT)} so‘m"
            )
            return

        # 3️⃣ Generate
        response = requests.post(
            "http://127.0.0.1:8000/api/generate-work/",
            json=data
        )

        if response.status_code != 200:
            bot.send_message(chat_id, "Serverda xatolik yuz berdi ❌")
            return

        resp_data = response.json()
        file_url = resp_data.get("file")

        if not file_url:
            bot.send_message(chat_id, "Fayl yaratilmay qoldi ❌")
            return

        # 4️⃣ MUHIM QISM — balansdan AYIRISH 🔥
        WorkUsage.objects.create(
            user=user,
            work_type=data.get("type", "referat"),
            amount=REQUIRED_AMOUNT
        )

        filename = os.path.basename(file_url)
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        with open(file_path, "rb") as f:
            bot.send_document(
                chat_id,
                f,
                caption="✅ Ish tayyor. Balansingizdan 4000 so‘m yechildi"
            )
            
            time.sleep(0.5)
            bot.send_message(chat_id, "Bosh menu", reply_markup=general_menu())

    elif call.data == "back":
        bot.send_message(chat_id, "Siz bosh menuga qaytingiz", reply_markup=general_menu())