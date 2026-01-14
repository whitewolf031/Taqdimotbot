from django.db.models import Sum
from taqdimot_app.models import User, Payment
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

    balance = Payment.objects.filter(
        user=user,
        status=True
    ).aggregate(total=Sum('amount'))['total'] or 0

    bot.send_message(
        chat_id,
        f"💰 Sizning balancingiz: {balance} so‘m",
        reply_markup=general_back()
    )
