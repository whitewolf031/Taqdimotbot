from telebot import types

def send_qollanma(bot, msg):
    text = (
        "🕹 *Buyruqlar va referal:*\n\n"
        "/my — ma'lumotlaringizni ko'rish uchun\n"
        "/new — yangi taqdimot tayyorlashni boshlash uchun\n"
        "/info — ma'lumot qidirish uchun\n"
        "/referat — referat tayyorlash bo‘limi\n"
        "/slide — slayd tayyorlash bo‘limi\n"
        "/buy — kartaga to‘lov qilish orqali balansni to‘ldirish\n"
        "/chek — to‘lovdan so‘ng chekni skrinshot qilib yuborish\n"
        "/vid — taqdimot uchun video qo‘llanma\n"
        "/video — referat / mustaqil ish uchun video qo‘llanma\n"
        "/help — ushbu qo‘llanma\n\n"
        "🔗 *Referal tizimi:*\n"
        "1️⃣ Har bir referal a'zo uchun — *1000 so'm*\n"
        "2️⃣ Referal a'zo har bir tayyorlagan taqdimot uchun — *100 so'm*\n"
        "3️⃣ Referal a'zo har bir to‘lovidan — *5% bonus*\n"
        "   (Masalan: 20 000 so‘m → 1000 so‘m)\n\n"
        "✍️ Chat: @eduslidebot_chat\n"
        "🆕 Bot yangilanishlari: @eduslidebot_news"
    )

    bot.send_message(
        chat_id=msg.chat.id,
        text=text,
        parse_mode="Markdown"
    )
