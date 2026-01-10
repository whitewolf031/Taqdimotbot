from telebot import types

def general_menu():
    keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
    slide = types.KeyboardButton("Slide tayorlash")
    referat = types.KeyboardButton("Referat/Amaliy ish")
    balance = types.KeyboardButton("Balance")
    info = types.KeyboardButton("Qo'llanma")
    keyboards.row(slide, referat)
    keyboards.row(balance, info)
    return keyboards