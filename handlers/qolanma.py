from telebot import types

def register_qollanma(bot):

    @bot.message_handler(commands=["Qo'llanma"])
    def send_qollanma(message):
        video_path = "taqdimot_app/videos/qollanma.mp4"

        caption = (
            "📘 *Botdan foydalanish qo‘llanmasi*\n\n"
            "• Referat olish\n"
            "• Slayd yaratish\n"
            "• Fan tanlash\n\n"
            "❓ Savollar bo‘lsa /contact"
        )

        with open(video_path, 'rb') as video:
            bot.send_video(
                chat_id=message.chat.id,
                video=video,
                caption=caption,
                parse_mode="Markdown"
            )
