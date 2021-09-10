from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from middlewares import i18n


_ = i18n.gettext


def new_invoice_markup() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
        [
            KeyboardButton(text=_("👛Получить")),
            KeyboardButton(text=_("💸Отдать"))
        ]
    ])
