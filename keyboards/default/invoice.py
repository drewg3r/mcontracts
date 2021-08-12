from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.misc import lang

new_invoice_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [
        KeyboardButton(text=lang.ru["new_invoice_keyboard_receive"]),
        KeyboardButton(text=lang.ru["new_invoice_keyboard_give"])
    ]
])
