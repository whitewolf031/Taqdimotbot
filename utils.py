from telebot import TeleBot, types

def private_only(func):
    def wrapper(message, *args, **kwargs):
        # faqat Message obyektida tekshirish
        if not hasattr(message, "chat"):
            return func(message, *args, **kwargs)  # agar bu string bo'lsa, dekorator tekshirmaydi

        if message.chat.type != "private":
            return  # Guruh va kanalni bloklash

        return func(message, *args, **kwargs)
    return wrapper