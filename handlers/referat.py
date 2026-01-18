from state.storage import user_state, user_data
from utils import private_only
from keyboards.botinlinekeyboards import referat_button, check_button, choose_languange
from keyboards.botreplykeyboards import betlar_soni, general_menu
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

@private_only
def start_referat(bot, msg):
    chat_id = msg.chat.id

    user_state[chat_id] = 'referat_topic'
    user_data[chat_id] = {}

    bot.send_message(chat_id, "Mavzuni to'liq, bexato va tushunarli qilib kiriting.")

@private_only
def referat_topic(bot, msg):
    chat_id = msg.chat.id

    user_data[chat_id]["topic"] = msg.text
    user_state[chat_id] = "referat_institute"

    bot.send_message(
        chat_id,
        "🏫 Institut va kafedrani kiriting (majburiy emas).\n"
        "Agar yo‘q bo‘lsa, `-` deb yozing."
    )

@private_only
def referat_institute(bot, msg):
    chat_id = msg.chat.id

    user_data[chat_id]["institute"] = msg.text
    user_state[chat_id] = "referat_author"

    bot.send_message(
        chat_id,
        "👤 Muallif ma’lumotlari (ISM, FAMILIYA, GURUH, KURS) ni to‘liq kiriting."
    )

@private_only
def referat_author(bot, msg):
    chat_id = msg.chat.id

    user_data[chat_id]["author"] = msg.text
    user_state[chat_id] = "referat_type"

    bot.send_message(
        chat_id,
        "📄 Ish turini tanlang:",
        reply_markup=referat_button()
    )

@private_only
def referat_type(bot, call):
    chat_id = call.message.chat.id
    user_data[chat_id]["type"] = call.data
    user_state[chat_id] = "referat_bet"

    bot.send_message(chat_id, "Varaqlar sonini tanlang", reply_markup=betlar_soni())

@private_only
def referat_bet(bot, msg):
    chat_id = msg.chat.id
    user_data[chat_id]["bet"] = msg.text
    type = user_data[chat_id]["type"]
    user_state[chat_id] = "referat_languange"

    bot.send_message(chat_id, f"{type} ni tilini tanlang.", reply_markup=choose_languange())

@private_only
def referat_languange(bot, call):
    chat_id = call.message.chat.id
    user_data[chat_id]["til"] = call.data
    user_state[chat_id] = "choose_button"

    data = user_data[chat_id]

    text = f"""🌟 Ajoyib, quyidagi ma’lumotlarni tekshiring.
        {data["type"].upper()}
        Mavzu: {data["topic"]}
        Institut va kafedra: {data['institute']}
        Muallif: {data['author']}

        Sahifalar soni: {data["bet"]}
        Tili: {data["til"]}

        ✅ Tayyorlash
        ✏️ O‘zgartirish
        🚫 Rad etish
    """

    bot.send_message(chat_id, text, reply_markup=check_button())

@private_only
def choose_button(bot, call):
    chat_id = call.message.chat.id
    data = user_data[chat_id]

    prompt = f"""
        REFERAT yozib ber:

        Mavzu: {data['topic']}
        Institut: {data['institute']}
        Muallif: {data['author']}
        Til: Uzbek
        Hajmi: 5–10 bet
    """

    if call.data == "do":
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Sen akademik referat yozuvchi yordamchisan."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    if call.data == "back":
        bot.send_message(chat_id, "Siz bosh menu dasiz", reply_markup=general_menu())
        return

    if call.data == "check":
        bot.send_message(chat_id, "Mavzuni to'liq, bexato va tushunarli qilib kiriting.")
        user_state[chat_id] = 'referat_topic'
        user_data[chat_id] = {}
