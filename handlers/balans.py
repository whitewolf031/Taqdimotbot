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

    # 1️⃣ Jami to‘lovlar
    total_paid = Payment.objects.filter(
        user=user,
        status=True
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

    # 2️⃣ Jami sarflangan summa
    total_used = WorkUsage.objects.filter(
        user=user
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

    # 3️⃣ Yakuniy balans
    balance = total_paid - total_used

    bot.send_message(
        chat_id,
        f"💰 Sizning balancingiz: {int(balance)} so‘m\n\n"
        f"➕ To‘lovlar: {int(total_paid)} so‘m\n"
        f"➖ Sarflangan: {int(total_used)} so‘m",
        reply_markup=general_back()
    )