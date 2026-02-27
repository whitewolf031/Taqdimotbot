from telebot import types

def send_qollanma(bot, msg):
    text = (
        "🕹 <b>Buyruqlar va referal:</b>\n\n"
        "/my — ma'lumotlaringizni ko'rish uchun\n"
        "/new — yangi taqdimot tayyorlashni boshlash uchun\n"
        "/referat — referat tayyorlash bo‘limi\n"
        "/slide — slayd tayyorlash bo‘limi\n"
        "/buy — kartaga to‘lov qilish orqali balansni to‘ldirish\n"
        "/vid — taqdimot uchun video qo‘llanma\n"
        "/video — referat / mustaqil ish uchun video qo‘llanma\n"
        "/help — ushbu qo‘llanma\n\n"
        "🔗 <b>Referal tizimi:</b>\n"
        "1️⃣ Har bir referal a'zo uchun — 4000 so'm\n"
        "2️⃣ Referal a'zo har bir tayyorlagan taqdimot uchun — 4000 so'm\n"
        "🧑🏻‍💻 Admin: @game_over272\n"
        "🆕 Bot yangilanishlari: @eduyordam"
    )

    bot.send_message(
        chat_id=msg.chat.id,
        text=text,
        parse_mode="HTML"
    )