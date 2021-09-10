from aiogram import Dispatcher

from loader import dp
from .language import setup_middleware
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    i18n = setup_middleware(dp)
    _ = i18n.gettext
