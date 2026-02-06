from payments.services.payment_ai_service import check_with_ai
from keyboards.botinlinekeyboards import send_check_button
from botconfig import BotConfig
from telebot import TeleBot, types
from taqdimot_app.models import User
from payments.models import Payment
from decimal import Decimal
from django.utils import timezone

bot = TeleBot(BotConfig().token)
ADMIN_ID = BotConfig().admin_id

@bot.message_handler(content_types=['photo'])
def receive_check_image(msg):
    chat_id = msg.chat.id
    file_id = msg.photo[-1].file_id

    bot.send_message(chat_id, "🔍 Chek tekshirilmoqda...")

    ai_result = check_with_ai(file_id)

    # ❌ AI chek deb topmadi
    if not ai_result["is_payment_receipt"] or ai_result["confidence"] < 0.8:
        bot.send_message(chat_id, "❌ Bu rasm to‘lov chekiga o‘xshamadi")
        return

    detected_amount = Decimal(str(ai_result.get("detected_amount") or "0"))

    # ❌ summa aniqlanmagan
    if detected_amount <= 0:
        bot.send_message(chat_id, "❌ Chekdagi summa aniqlanmadi")
        return

    # user yaratish / olish
    user, _ = User.objects.get_or_create(
        chat_id=chat_id,
        defaults={
            "first_name": msg.from_user.first_name or "",
            "last_name": msg.from_user.last_name or "",
            "username": msg.from_user.username,
        }
    )

    # payment yaratish (status = pending)
    payment = Payment.objects.create(
        user=user,
        amount=detected_amount,
        method="manual",
        status="pending",
        receipt_file_id=file_id,
        verified_by_ai=True
    )

    bot.send_message(chat_id, "✅ Chek qabul qilindi. Admin tasdiqlaydi.")

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
        caption=(
            f"🧾 Payment #{payment.id}\n"
            f"👤 User: {payment.user.chat_id}\n"
            f"💰 Summa: {payment.amount} so‘m\n"
            f"🤖 AI: {'Ha' if payment.verified_by_ai else 'Yo‘q'}"
        ),
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith(("approve_", "reject_")))
def admin_decision(call):
    action, payment_id = call.data.split("_")

    try:
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        bot.answer_callback_query(call.id, "Payment topilmadi")
        return

    # ❗ allaqachon tekshirilganmi?
    if payment.status != "pending":
        bot.answer_callback_query(call.id, "Bu to‘lov allaqachon tekshirilgan")
        return

    # ✅ APPROVE
    if action == "approve":
        payment.status = "approved"
        payment.confirmed_at = timezone.now()
        payment.save()

        bot.send_message(
            payment.user.chat_id,
            f"✅ To‘lov tasdiqlandi!\n💰 {payment.amount} so‘m balansga qo‘shildi."
        )

        bot.edit_message_caption(
            caption=call.message.caption + "\n\n✅ TASDIQLANDI",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )

    # ❌ REJECT
    else:
        payment.status = "rejected"
        payment.save()

        bot.send_message(
            payment.user.chat_id,
            "❌ To‘lov rad etildi.\nIltimos to‘g‘ri chek yuboring."
        )

        bot.edit_message_caption(
            caption=call.message.caption + "\n\n❌ RAD ETILDI",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )

    bot.answer_callback_query(call.id, "Bajarildi")