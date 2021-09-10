from aiogram import types
from aiogram.dispatcher.filters.builtin import Command

from loader import dp
from middlewares import i18n
from utils.templates import t

_ = i18n.gettext


@dp.message_handler(Command("help"))
async def bot_help(message: types.Message):
    await message.answer(_(t["/help"]))
