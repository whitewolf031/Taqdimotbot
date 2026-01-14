from state.storage import user_state
from handlers.contact import take_phone, user_message, commit_message
from keyboards.botreplykeyboards import general_menu
from utils import private_only

def register_state_manager(bot):
    @bot.message_handler(
        func=lambda m: user_state.get(m.chat.id) is not None,
        content_types=['text', 'contact']
    )
    @private_only
    def state_manager(msg):
        chat_id = msg.chat.id
        state = user_state.get(chat_id)

        if msg.text == "Orqaga":
            user_state.pop(chat_id, None)
            bot.send_message(chat_id, "🏠 Menu", reply_markup=general_menu())
            return

        if state == "take_phone":
            take_phone(bot, msg)

        elif state == "user_message":
            user_message(bot, msg)

        elif state == "commit_message":
            commit_message(bot, msg)