from aiogram import Dispatcher
from loguru import logger

from data import config


async def on_startup_notify(dp: Dispatcher):
    try:
        for admin in config.ADMINS:
            await dp.bot.send_message(admin, "Bot started")
    except Exception as err:
        logger.opt(exception=err).error("Broad Exception")
