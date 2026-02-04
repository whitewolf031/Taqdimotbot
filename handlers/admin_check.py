from payments.services.payment_ai_service import check_with_ai
from keyboards.botinlinekeyboards import send_check_button
from botconfig import BotConfig
from telebot import TeleBot, types
from taqdimot_app.models import User
from payments.models import Payment
from payments.services.payment_ai_service import check_with_ai
from decimal import Decimal

bot = TeleBot(BotConfig().token)

ADMIN_ID = BotConfig().admin_id

@bot.message_handler(content_types=['photo'])
def receive_check_image(msg):
    chat_id = msg.chat.id
    file_id = msg.photo[-1].file_id

    bot.send_message(chat_id, "🔍 Rasm tekshirilmoqda, iltimos kuting...")

    ai_result = check_with_ai(file_id)

    if not ai_result["is_payment_receipt"] or ai_result["confidence"] < 0.8:
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
        amount=Decimal(str(ai_result.get("detected_amount") or "0")),
        method="manual",
        status="pending",
        receipt_file_id=file_id,
        verified_by_ai=True
    )

    bot.send_message(chat_id, "✅ Chek qabul qilindi, admin tekshiradi")

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