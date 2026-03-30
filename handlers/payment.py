# # handlers/payment.py
# from telebot import types
# from django.utils import timezone
# from decimal import Decimal
# from taqdimot_app.models import User
# from payments.models import Payment
# from botconfig import BotConfig
# import os
# from dotenv import load_dotenv

# load_dotenv()
# provider_token = os.getenv("PAYME_PROVIDER_TOKEN")

# def send_payme_invoice_by_chat(bot, chat_id, amount):
#     """
#     Foydalanuvchi kiritgan summaga invoice jo'natish
#     """
#     amount = int(amount)
#     prices = [
#         types.LabeledPrice(
#             label=f"Balans to‘ldirish ({amount} so‘m)",
#             amount=amount * 100  # Telegram cent birligi
#         )
#     ]

#     bot.send_invoice(
#         chat_id=chat_id,
#         title="Balans to‘ldirish",
#         description="Referat va slaydlar uchun balans",
#         provider_token=provider_token,
#         currency="UZS",
#         prices=prices,
#         start_parameter="balance_top_up",
#         invoice_payload=f"balance_{amount}",
#     )


# def pre_checkout_handler(bot, query):
#     """ Telegram tekshiruvi """
#     bot.answer_pre_checkout_query(query.id, ok=True)


# def successful_payment_handler(bot, msg):
#     """ Muvaffaqiyatli to‘lovdan so‘ng DB ga yozish """
#     chat_id = msg.chat.id
#     amount = msg.successful_payment.total_amount // 100

#     user, _ = User.objects.get_or_create(
#         chat_id=chat_id,
#         defaults={
#             "first_name": msg.from_user.first_name or "",
#             "last_name": msg.from_user.last_name or "",
#             "username": msg.from_user.username,
#         }
#     )

#     Payment.objects.create(
#         user=user,
#         amount=Decimal(amount),
#         method="payme",
#         status=True,  # true qilib saqlaymiz
#         confirmed_at=timezone.now()
#     )

#     bot.send_message(
#         chat_id,
#         f"✅ To‘lov muvaffaqiyatli!\n💰 {amount} so‘m balansingizga qo‘shildi"
#     )