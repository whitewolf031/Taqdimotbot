from django.db.models import Sum
from decimal import Decimal
from taqdimot_app.models import User
from payments.models import Payment, WorkUsage
from keyboards.botreplykeyboards import general_back
from utils import private_only

@private_only
def show_balance(bot, msg):
    chat_id = msg.chat.id

    try:
        user = User.objects.get(chat_id=chat_id)
    except User.DoesNotExist:
        bot.send_message(
            chat_id,
            "❌ Siz hali ro‘yxatdan o‘tmagansiz.",
            reply_markup=general_back()
        )
        return

    # 1️⃣ Faqat TASDIQLANGAN to‘lovlar yig‘indisi
    total_paid = (
        Payment.objects
        .filter(user=user, status="approved")
        .aggregate(total=Sum("amount"))["total"]
        or Decimal("0")
    )

    # 2️⃣ Jami sarflangan summa
    total_used = (
        WorkUsage.objects
        .filter(user=user)
        .aggregate(total=Sum("amount"))["total"]
        or Decimal("0")
    )

    # 3️⃣ Yakuniy balans
    balance = total_paid - total_used

    bot.send_message(
        chat_id,
        "💰 <b>Sizning balancingiz</b>\n\n"
        f"💵 Balans: <b>{balance:,.0f}</b> so‘m\n\n"
        f"➕ To‘langan: {total_paid:,.0f} so‘m\n"
        f"➖ Sarflangan: {total_used:,.0f} so‘m",
        parse_mode="HTML",
        reply_markup=general_back()
    )