from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from middlewares import i18n

_ = i18n.gettext


def choose_language_markup():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="English", callback_data="change_lang:en"),
            InlineKeyboardButton(text="Русский", callback_data="change_lang:ru"),
            InlineKeyboardButton(text="Українська", callback_data="change_lang:uk")
        ]
    ])
