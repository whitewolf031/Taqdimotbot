from telebot import types

def referat_button():
    keyboards = types.InlineKeyboardMarkup()
    referat = types.InlineKeyboardButton(text="Referat", callback_data='referat')
    mustaqil_ish = types.InlineKeyboardButton(text="Mustaqil ish", callback_data="mustaqil_ish")
    keyboards.row(referat, mustaqil_ish)
    return keyboards

def check_button():
    keyboards = types.InlineKeyboardMarkup()
    do = types.InlineKeyboardButton(text="Tayyorlash", callback_data='referat_do')
    cancel = types.InlineKeyboardButton(text="Rad etish", callback_data="referat_back")
    check = types.InlineKeyboardButton(text="O'zgartirish", callback_data="referat_check")
    keyboards.row(do, cancel, check)
    return keyboards

def slide_button():
    keyboards = types.InlineKeyboardMarkup()
    do = types.InlineKeyboardButton(text="Tayyorlash", callback_data='slide_do')
    cancel = types.InlineKeyboardButton(text="Rad etish", callback_data="slide_back")
    check = types.InlineKeyboardButton(text="O'zgartirish", callback_data="slide_check")
    keyboards.row(do, cancel, check)
    return keyboards

def choose_languange():
    keyboards = types.InlineKeyboardMarkup()
    uzbek = types.InlineKeyboardButton(text="UZ", callback_data='referat_uz')
    engilish = types.InlineKeyboardButton(text="ENG", callback_data="referat_eng")
    rus = types.InlineKeyboardButton(text="RU", callback_data="referat_ru")
    keyboards.row(uzbek, engilish, rus)
    return keyboards

def slide_lang():
    keyboards = types.InlineKeyboardMarkup()
    uzbek = types.InlineKeyboardButton(text="UZ", callback_data='slide_uz')
    engilish = types.InlineKeyboardButton(text="ENG", callback_data="slide_en")
    rus = types.InlineKeyboardButton(text="RU", callback_data="slide_ru")
    keyboards.row(uzbek, engilish, rus)
    return keyboards

def payme_button():
    keyboards = types.InlineKeyboardMarkup()
    payme = types.InlineKeyboardButton(text="💳 Payme orqali to‘lash", callback_data="pay_4000")
    keyboards.row(payme)
    return keyboards

def pay_type():
    keyboards = types.InlineKeyboardMarkup()
    click = types.InlineKeyboardButton(text="💳 Plastik dan click qilish", callback_data="click")
    keyboards.row(click)
    return keyboards

def send_check_button():
    keyboards = types.InlineKeyboardMarkup()
    send_check = types.InlineKeyboardButton(text="Check ni jo'natish", callback_data="send_check")
    back = types.InlineKeyboardButton(text="Orqaga", callback_data="check_back")
    keyboards.row(send_check)
    keyboards.row(back)
    return keyboards

def payme_cash():
    keyboards = types.InlineKeyboardMarkup()
    # Har bir tugma uchun alohida callback_data
    boshlangich = types.InlineKeyboardButton(text="5 000", callback_data="pay_5000")
    orta = types.InlineKeyboardButton(text="10 000", callback_data="pay_10000")
    eng_orta = types.InlineKeyboardButton(text="20 000", callback_data="pay_20000")
    yuqori = types.InlineKeyboardButton(text="50 000", callback_data="pay_50000")
    boshqa = types.InlineKeyboardButton(text="Boshqa summa", callback_data="pay_boshqa")
    
    keyboards.row(boshlangich, orta)
    keyboards.row(eng_orta, yuqori)
    keyboards.row(boshqa)
    return keyboards