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
from django.db import transaction

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

    text = text = f"""
    🌟 Ajoyib, quyidagi ma’lumotlarni tekshiring.

    <b>{data["type"].upper()}</b>
    <b>Mavzu: {data["topic"]}</b>
    <b>Institut va kafedra:</b> {data['institute']}
    <b>Muallif:</b> {data['author']}
    <b>Sahifalar soni:</b> {data["bet"]}
    <b>Tili:</b> {data["til"]}
    <b>Hajmi:</b> {data['bet']} bet

    <b>✅ Tayyorlash</b>
    <b>✏️ O‘zgartirish</b>
    <b>🚫 Rad etish</b>
    """
    
    bot.send_message(chat_id, text, reply_markup=check_button(), parse_mode="HTML")

@private_only
def choose_button(bot, call):
    chat_id = call.message.chat.id

    # ❗ Sessiya yo‘q bo‘lsa crash bo‘lmasin
    if chat_id not in user_data:
        bot.send_message(chat_id, "Sessiya tugagan. Qaytadan boshlang.")
        bot.send_message(chat_id, "Bosh menu", reply_markup=general_menu())
        return

    data = user_data[chat_id]

    # 🔙 BACK tugmasi
    if call.data == "back":
        user_data.pop(chat_id, None)
        user_state.pop(chat_id, None)
        bot.send_message(chat_id, "Bosh menu", reply_markup=general_menu())
        return

    # 🚀 GENERATE
    if call.data != "do":
        return

    # 1️⃣ USER olish yoki yaratish
    user, _ = User.objects.get_or_create(
        chat_id=chat_id,
        defaults={
            "first_name": call.message.chat.first_name or "",
            "last_name": call.message.chat.last_name,
            "username": call.message.chat.username,
        }
    )

    # 2️⃣ REAL BALANS HISOBLASH (approved Payment summalari orqali)
    payments_sum = Payment.objects.filter(
        user=user,
        status="approved"
    ).aggregate(total=Sum("amount"))["total"] or 0

    used_sum = WorkUsage.objects.filter(user=user).aggregate(total=Sum("amount"))["total"] or 0

    balance = Decimal(payments_sum) - Decimal(used_sum)

    if balance < REQUIRED_AMOUNT:
        bot.send_message(
            chat_id,
            f"❌ Mablag‘ yetarli emas\n\n"
            f"💰 Balans: {balance:,.0f} so‘m\n"
            f"📌 Kerakli: {REQUIRED_AMOUNT:,.0f} so‘m"
        )
        return

    # WorkUsage choices ga moslab olamiz
    work_type = data.get("type", "referat").lower()
    if work_type not in ["referat", "mustaqil"]:
        work_type = "referat"

    try:
        # ❗ TRANSACTION ICHIDA barcha kritik ishlar
        with transaction.atomic():
            # 3️⃣ ISH GENERATSIYA API
            response = requests.post(
                "http://127.0.0.1:8000/api/generate-work/",
                json=data,
                timeout=180
            )

            if response.status_code != 200:
                raise Exception("API error")

            resp_data = response.json()
            file_url = resp_data.get("file")

            if not file_url:
                raise Exception("File not generated")

            # 4️⃣ BALANSDAN YECHISH
            WorkUsage.objects.create(
                user=user,
                work_type=work_type,
                amount=REQUIRED_AMOUNT
            )

    except Exception as e:
        print("OPENAI ERROR:", e)
        bot.send_message(chat_id, f"❌ Serverda xatolik yuz berdi: {e}")
        return

    # ✅ FAYL YUBORISH
    filename = os.path.basename(file_url)
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    try:
        with open(file_path, "rb") as f:
            bot.send_document(
                chat_id,
                f,
                caption=(
                    "✅ Ish tayyor!\n"
                    f"💸 Balansingizdan {REQUIRED_AMOUNT:,.0f} so‘m yechildi"
                )
            )
    except Exception as e:
        bot.send_message(chat_id, f"Faylni yuborishda xatolik: {e}")

    # 5️⃣ STATE TOZALASH
    user_data.pop(chat_id, None)
    user_state.pop(chat_id, None)

    time.sleep(0.3)
    bot.send_message(chat_id, "Bosh menu", reply_markup=general_menu())