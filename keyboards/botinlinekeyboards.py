from telebot import types

def referat_button():
    keyboards = types.InlineKeyboardMarkup()
    referat = types.InlineKeyboardButton(text="Referat", callback_data='referat')
    mustaqil_ish = types.InlineKeyboardButton(text="Mustaqil ish", callback_data="mustaqil_ish")
    keyboards.row(referat, mustaqil_ish)
    return keyboards

def check_button():
    keyboards = types.InlineKeyboardMarkup()
    do = types.InlineKeyboardButton(text="Tayyorlash", callback_data='do')
    cancel = types.InlineKeyboardButton(text="Rad etish", callback_data="back")
    check = types.InlineKeyboardButton(text="O'zgartirish", callback_data="check")
    keyboards.row(do, cancel, check)
    return keyboards

def choose_languange():
    keyboards = types.InlineKeyboardMarkup()
    uzbek = types.InlineKeyboardButton(text="UZ", callback_data='uz')
    engilish = types.InlineKeyboardButton(text="ENG", callback_data="eng")
    rus = types.InlineKeyboardButton(text="RU", callback_data="ru")
    keyboards.row(uzbek, engilish, rus)
    return keyboards