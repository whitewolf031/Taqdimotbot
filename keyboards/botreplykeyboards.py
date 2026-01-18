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

def betlar_soni():
    keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bet1 = types.KeyboardButton("5-10")
    bet2 = types.KeyboardButton("10-15")
    bet3 = types.KeyboardButton("15-20")
    bet4 = types.KeyboardButton("20-25")
    bet5 = types.KeyboardButton("25-30")
    bet6 = types.KeyboardButton("30-35")

    keyboards.row(bet1, bet2)
    keyboards.row(bet3, bet4)
    keyboards.row(bet5, bet6)
    
    return keyboards
