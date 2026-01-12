from telebot import types

def general_menu():
    keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
    slide = types.KeyboardButton("Slide tayorlash")
    referat = types.KeyboardButton("Referat/Amaliy ish")
    balance = types.KeyboardButton("Balance")
    info = types.KeyboardButton("Qo'llanma")
    contact = types.KeyboardButton("Bog'lanish")
    keyboards.row(slide, referat)
    keyboards.row(balance, info)
    keyboards.row(contact)
    return keyboards

def take_contact():
    keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
    contact_button = types.KeyboardButton("Phone number", request_contact=True)
    keyboards.row(contact_button)
    return keyboards

def general_back():
    keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("Orqaga")
    keyboards.row(back)
    return keyboards