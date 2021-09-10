import peewee
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loguru import logger

from loader import dp
from middlewares import i18n
from utils.db_api.models import User

_ = i18n.gettext


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        User.get(User.telegram_id == message.from_user.id)
    except peewee.DoesNotExist:
        locale = message.from_user.language_code if message.from_user.language_code in ["en", "ru", "uk"] else "en"
        User.create(telegram_id=message.from_user.id, locale=locale)
        logger.info("New User({}, #{}) registered!".format(message.from_user.full_name, message.from_user.id))
    finally:
        await message.answer(_("Добро пожаловать, {name}!\nВведите /help для получения справки").
                             format(name=message.from_user.first_name))
