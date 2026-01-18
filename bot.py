from telebot import TeleBot
from handlers.start import start_handler
from handlers.contact import admin_contact, take_phone, user_message, commit_message
from handlers.balans import show_balance
from handlers.referat import start_referat, referat_type, referat_languange, referat_button
from botconfig import BotConfig
from state.state_meneger import register_state_manager
from state.storage import user_state
from keyboards.botreplykeyboards import general_menu
from handlers.slide import slide_handler
from  handlers.qolanma import send_qollanma

def start_bot():

    bot = TeleBot(BotConfig().token)

    register_state_manager(bot)

    start_handler(bot)
    slide_handler(bot)

    @bot.message_handler(func=lambda m: m.text == "Qo'llanma")
    def qollanma_handler(msg):
        send_qollanma(bot, msg)

    @bot.message_handler(commands=['referat'])
    def referat(msg):
        start_referat(bot, msg)

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

    @bot.callback_query_handler(func=lambda call: call.data in ["referat","mustaqil_ish"])
    def path_function(call):
        referat_type(bot, call)

    @bot.callback_query_handler(func=lambda call: call.data in ["uz","eng", "ru"])
    def referat_lang(call):
        referat_languange(bot, call)

    @bot.callback_query_handler(func=lambda call: call.data in ["do","back", "check"])
    def referat_do(call):
        referat_button(bot, call)

    @bot.message_handler(func=lambda m: m.text in ("Orqaga", "Orqaga ⬅️"))
    def go_back(msg):
        chat_id = msg.chat.id
        user_state.pop(chat_id, None)
        bot.send_message(chat_id, "🏠 Menu", reply_markup=general_menu())


    print("Telegram bot ishga tushdi...")
    bot.infinity_polling(skip_pending=True)