import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # <-- o'zingizning settings.py joyi
django.setup()

# ────────────────────────────────────────────────────────────────────
import socket

original_getaddrinfo = socket.getaddrinfo

def getaddrinfo_ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
    return original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

socket.getaddrinfo = getaddrinfo_ipv4_only
# ────────────────────────────────────────────────────────────────────

from telebot import TeleBot
from handlers.start import start_handler
from handlers.contact import admin_contact, take_phone, user_message, commit_message
from handlers.balans import show_balance
from handlers.referat import start_referat, referat_type, referat_languange, choose_button
from botconfig import BotConfig
from state.state_meneger import register_state_manager
from state.storage import user_state
from keyboards.botreplykeyboards import general_menu
from keyboards.botinlinekeyboards import payme_cash, pay_type, send_check_button
from handlers.slide import send_slide, slide_confirm, slide_send_button
from handlers.admin_check import receive_check_image
from handlers.qolanma import send_qollanma
# from handlers.payment import (
#     send_payme_invoice_by_chat,
#     pre_checkout_handler,
#     successful_payment_handler
# )

bot = TeleBot(BotConfig().token)

register_state_manager(bot)

start_handler(bot)

@bot.message_handler(func=lambda m: m.text == "Qo'llanma")
def qollanma_handler(msg):
    send_qollanma(bot, msg)

@bot.message_handler(commands=['referat'])
def referat(msg):
    start_referat(bot, msg)

@bot.message_handler(commands=['slide'])
def slide_command(msg):
    send_slide(bot, msg)

# Oddiy menu handlerlar
@bot.message_handler(func=lambda m: m.text == "Bog'lanish")
def contact_handler(msg):
    admin_contact(bot, msg)  # ✅ botni uzatish

@bot.message_handler(func=lambda m: m.text == "Balance")
def balance_handler(msg):
    show_balance(bot, msg)

@bot.message_handler(func=lambda m: m.text == "Referat/Amaliy ish")
def referat_handler(msg):
    start_referat(bot, msg)

@bot.message_handler(func=lambda m: m.text == "Slide tayorlash")
def slide_handler(msg):
    send_slide(bot, msg)

@bot.callback_query_handler(func=lambda call: call.data in ["referat","mustaqil_ish"])
def path_function(call):
    referat_type(bot, call)

@bot.callback_query_handler(func=lambda call: call.data in ["referat_uz","referat_eng", "referat_ru"])
def referat_lang(call):
    referat_languange(bot, call)

@bot.callback_query_handler(func=lambda call: call.data in ["slide_uz","slide_en", "slide_ru"])
def slide_language(call):
    slide_confirm(bot, call)

@bot.callback_query_handler(func=lambda call: call.data in ["referat_do","referat_back", "referat_check"])
def referat_do(call):
    choose_button(bot, call)

@bot.callback_query_handler(func=lambda call: call.data in ["slide_do","slide_back", "slide_check"])
def slide_do(call):
    slide_send_button(bot, call)

# PAYME CALLBACK
@bot.message_handler(commands=['buy'])
def buy_command(msg):
    chat_id = msg.chat.id
    bot.send_message(
        chat_id,
        "To'lov turini tanlang",
        reply_markup=pay_type()
    )

@bot.callback_query_handler(func=lambda call: call.data in ["click","bot_pay"])
def payment_type_handler(call):
    chat_id = call.message.chat.id

    if call.data == "click":
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

    if call.data == "bot_pay":
        bot.send_message(
        chat_id,
        "💰 Iltimos, to‘lamoqchi bo‘lgan summani tanlang yoki boshqa summani kiriting:",
        reply_markup=payme_cash()
    )

    
@bot.callback_query_handler(func=lambda call: call.data in ["send_check", "check_back"])
def send_check_handler(call):
    bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id

    if call.data == "send_check":
        bot.send_message(
            chat_id,
            "📸 Iltimos, to‘lov chekini (screenshot) yuboring.\n\n"
            "❗️Faqat to‘lov amalga oshirilganini ko‘rsatadigan rasm bo‘lsin."
        )
        bot.register_next_step_handler(call.message, receive_check_image)

# @bot.callback_query_handler(func=lambda call: call.data.startswith("pay_"))
# def pay_callback(call):
#     chat_id = call.message.chat.id
#     data = call.data
#     if data == "pay_boshqa":
#         bot.send_message(chat_id, "💰 Iltimos, to‘lamoqchi bo‘lgan summani kiriting:")
#         bot.register_next_step_handler(call.message, ask_amount)
    
#     else:
#         # callback_data dan summani ajratamiz
#         amount = int(data.split("_")[1])
#         send_payme_invoice_by_chat(bot, chat_id, amount)

# def ask_amount(msg):
#     chat_id = msg.chat.id
#     try:
#         amount = int(msg.text.replace(" ", ""))
#         if amount < 100:
#             bot.send_message(chat_id, "❌ Summa juda kichik, iltimos kattaroq summa kiriting")
#             return
#     except ValueError:
#         bot.send_message(chat_id, "❌ Iltimos, faqat raqam kiriting")
#         return
    
#     # Invoice jo'natamiz
#     send_payme_invoice_by_chat(bot, chat_id, amount)

# @bot.pre_checkout_query_handler(func=lambda query: True)
# def pre_checkout(query):
#     pre_checkout_handler(bot, query)

# @bot.message_handler(content_types=['successful_payment'])
# def success_payment(msg):
#     successful_payment_handler(bot, msg)

@bot.message_handler(func=lambda m: m.text in ("Orqaga", "Orqaga ⬅️"))
def go_back(msg):
    chat_id = msg.chat.id
    user_state.pop(chat_id, None)
    bot.send_message(chat_id, "🏠 Menu", reply_markup=general_menu())

print("Telegram bot ishga tushdi...")
bot.infinity_polling(skip_pending=True)