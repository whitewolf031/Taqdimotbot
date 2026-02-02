from payments.services.payment_ai_service import check_with_ai
from keyboards.botinlinekeyboards import send_check_button
from botconfig import BotConfig
from telebot import TeleBot

bot = TeleBot(BotConfig().token)

ADMIN_ID = BotConfig().admin_id

def admin_check_handler(bot, call):
    chat_id = call.message.chat.id

    click_text = (
            "❗Balansingizni to'ldirish uchun quyidagi karta raqamiga to'lov qiling va chekni skrenshot qilib oling (COPY qilish uchun karta raqam ustiga bosing).\n\n"
            "💳 plastik\n"
            "👤 Saitmurodova Zaynura\n\n"
            "🧾To'lov qilganingizdan so'ng /chek buyrug'ini yuboring yoki quyidagi tugmani bosing👇"
    )

    bot.send_message(
        chat_id,
        click_text,
        reply_markup=send_check_button()
    )

@bot.callback_query_handler(func=lambda call: call.data in ["send_check", "check_back"])
def ask_screenshot(call):
    chat_id = call.message.chat.id

    bot.send_message(
        chat_id,
        "📸 Iltimos, to‘lov chekini (screenshot) yuboring.\n\n"
        "❗️Faqat to‘lov amalga oshirilganini ko‘rsatadigan rasm bo‘lsin."
    )

    # keyingi qadam — rasm qabul qilish
    bot.register_next_step_handler(call.message, receive_check_image)

def receive_check_image(msg):
    chat_id = msg.chat.id

    if not msg.photo:
        bot.send_message(chat_id, "❌ Iltimos, rasm yuboring")
        return

    file_id = msg.photo[-1].file_id

    ai_result = check_with_ai(file_id)

    if not ai_result["looks_like_payment"]:
        bot.send_message(chat_id, "❌ Bu rasm to‘lov chekiga o‘xshamadi")
        return

    user, _ = User.objects.get_or_create(
        chat_id=chat_id,
        defaults={
            "first_name": msg.from_user.first_name or "",
            "last_name": msg.from_user.last_name or "",
            "username": msg.from_user.username,
        }
    )

    payment = Payment.objects.create(
        user=user,
        amount=Decimal(ai_result.get("detected_amount") or 0),
        method="manual",
        status="pending",
        receipt_file_id=file_id,
        verified_by_ai=True
    )

    send_to_admin_for_approval(payment)

def send_to_admin_for_approval(payment):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"approve_{payment.id}"),
        types.InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_{payment.id}")
    )

    bot.send_photo(
        ADMIN_ID,
        payment.receipt_file_id,
        caption=f"🧾 Payment #{payment.id}\n"
                f"👤 {payment.user.chat_id}\n"
                f"💰 {payment.amount} so‘m",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith(("approve_", "reject_")))
def admin_decision(call):
    action, payment_id = call.data.split("_")
    payment = Payment.objects.get(id=payment_id)

    if action == "approve":
        payment.status = "approved"
        payment.confirmed_at = timezone.now()
        payment.save()

        bot.send_message(
            payment.user.chat_id,
            f"✅ To‘lov tasdiqlandi: {payment.amount} so‘m"
        )
        bot.send_message(call.message.chat.id, "✅ Tasdiqlandi")

    else:
        payment.status = "rejected"
        payment.save()

        bot.send_message(
            payment.user.chat_id,
            "❌ To‘lov rad etildi. Check noto‘g‘ri."
        )
        bot.send_message(call.message.chat.id, "❌ Rad etildi")