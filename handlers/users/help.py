from aiogram import types
from aiogram.dispatcher.filters.builtin import Command

from loader import dp
from utils.misc import lang


@dp.message_handler(Command("help"))
async def bot_help(message: types.Message):
    await message.answer(lang.ru["/help"])
