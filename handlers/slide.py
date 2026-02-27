from state.storage import user_slide, user_state
from utils import private_only
from keyboards.botinlinekeyboards import slide_button, slide_lang
from keyboards.botreplykeyboards import general_menu
from django.conf import settings
from taqdimot_app.models import User
from payments.models import Payment, WorkUsage
from django.db.models import Sum
from decimal import Decimal
from taqdimot_app.services import balance_service
import time
from django.db import transaction
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

REQUIRED_AMOUNT = Decimal("4000")

def send_slide(bot, msg):
    chat_id = msg.chat.id

    user_state[chat_id] = 'author_name'
    user_slide[chat_id] = {}

    slide_text = (f"Slide mavzusini bexato va aniq qilib kiriting.")

    bot.send_message(chat_id, slide_text, parse_mode="HTML")

def author_name(bot, msg):
    chat_id = msg.chat.id
    user_slide[chat_id]["topic"] = msg.text
    user_state[chat_id] = "slide_insitut"

    slide_insitut_text = ("Institut va kafedrangizni(majburiy emas) to'liq kiriting.\n\n"
            "Misol: <b>O‘ZBEKISTON RESPUBLIKASI OLIY TA’LIM FAN VA INNOVATSIYA VAZIRLIGI"
                        "SARBON UNIVERSITETI"
                        "AXBOROT XAVFSIZLIGI KAFEDRASI.</b>")

    bot.send_message(chat_id, slide_insitut_text, parse_mode="HTML")

def slide_insitut(bot, msg):
    chat_id = msg.chat.id

    user_slide[chat_id]["institute"] = msg.text
    user_state[chat_id] = "slide_author"

    mualif = ("Muallif ism-familiyasi, guruhi va kursini to'liq kiriting.\n\n"
            "📋Namuna: <b>Isroilov Ismoiljon Muhiddin o'g'li, 4-kurs, 21.36-guruh.</b>")

    bot.send_message(
        chat_id,
        mualif,
        parse_mode="HTML"
    )

def slide_author(bot, msg):
    chat_id = msg.chat.id
    user_slide[chat_id]["author"] = msg.text
    user_state[chat_id] = "slide_bet"

    bot.send_message(chat_id, "Slide lar betini kiriting")

def slide_bet(bot, msg):
    chat_id = msg.chat.id

    # 1️⃣ Raqam emas bo‘lsa ushlaymiz
    try:
        slide_bet_int = int(msg.text)
    except ValueError:
        user_state[chat_id] = "slide_bet"
        bot.send_message(chat_id, "❌ Iltimos faqat raqam kiriting (6 - 20)")
        return

    # 2️⃣ 6 dan kichik bo‘lsa
    if slide_bet_int < 6:
        user_state[chat_id] = "slide_bet"
        bot.send_message(chat_id, "❌ Slide 6 betdan kam bo‘lmasligi kerak.\n\nQayta kiriting:")
        return

    # 3️⃣ 20 dan katta bo‘lsa
    if slide_bet_int > 20:
        user_state[chat_id] = "slide_bet"
        bot.send_message(chat_id, "❌ Slide 20 betdan ko‘p bo‘lmasligi kerak.\n\nQayta kiriting:")
        return

    # 4️⃣ To‘g‘ri kiritildi ✅
    user_slide[chat_id]["bet"] = slide_bet_int
    user_state[chat_id] = "slide_language"

    bot.send_message(chat_id, "Tilni tanlang", reply_markup=slide_lang())

@private_only
def slide_confirm(bot, call):
    chat_id = call.message.chat.id
    user_slide[chat_id]["til"] = call.data
    user_state[chat_id] = "choose_button"

    data = user_slide[chat_id]

    text = (f"🌟 Ajoyib, quyidagi ma’lumotlarni tekshiring.\n\n"
        f"<b>Slide</b>\n"
        f"<b>Mavzu: {data["topic"]}</b>\n"
        f"<b>Institut va kafedra:</b> {data['institute']}\n"
        f"<b>Muallif:</b> {data['author']}\n"
        f"<b>Sahifalar soni:</b> {data["bet"]}\n"
        f"<b>Tili:</b> {data["til"]}\n\n"
        f"<b>✅ Tayyorlash</b>\n"
        f"<b>✏️ O‘zgartirish</b>\n"
        "<b>🚫 Rad etish</b>")

    bot.send_message(chat_id, text, reply_markup=slide_button(), parse_mode="HTML")

@private_only
def slide_send_button(bot, call):
    chat_id = call.message.chat.id

    # ❗ Sessiya yo‘q bo‘lsa crash bo‘lmasin
    if chat_id not in user_slide:
        bot.send_message(chat_id, "Sessiya tugagan. Qaytadan boshlang.")
        bot.send_message(chat_id, "Bosh menu", reply_markup=general_menu())
        return

    data = user_slide[chat_id]

    # 🔙 BACK tugmasi
    if call.data == "back":
        user_slide.pop(chat_id, None)
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