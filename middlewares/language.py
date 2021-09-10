import peewee
from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from loguru import logger

from data.config import I18N_DOMAIN, LOCALES_DIR
from utils.db_api.models import User
from utils.exceptions import UserNotFoundException


def get_lang(telegram_user_id: int) -> str:
    try:
        user = User.get(User.telegram_id == telegram_user_id)
    except peewee.DoesNotExist:
        logger.error("User#{} not found in DB while getting his locale".format(telegram_user_id))
        raise UserNotFoundException
    return user.locale


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action, args) -> str:
        user = types.User.get_current()
        try:
            return get_lang(user.id)
        except UserNotFoundException:
            logger.error("Returning RU locale")
            return "en"


def setup_middleware(dp):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    logger.debug("i18n middleware setup done")
    return i18n
