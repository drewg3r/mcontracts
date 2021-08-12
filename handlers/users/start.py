import peewee
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loguru import logger

from loader import dp
from utils.db_api.models import User
from utils.misc import lang


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        User.get(User.telegram_id == message.from_user.id)
    except peewee.DoesNotExist:
        User.create(telegram_id=message.from_user.id, locale=message.from_user.language_code)
        logger.info("New User({}, #{}) registered!".format(message.from_user.full_name, message.from_user.id))
    finally:
        await message.answer(lang.ru["/start"].format(name=message.from_user.first_name))
