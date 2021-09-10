from aiogram import executor
from loguru import logger

from loader import dp, db
import middlewares, handlers
from utils.db_api.models import User, Contract, UserToContractConnector, Invoice
from utils.misc.on_startup_notify import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    db.create_tables([User, Contract, UserToContractConnector, Invoice])
    logger.success("Polling started")


if __name__ == '__main__':
    logger.info("Starting polling")
    executor.start_polling(dp, on_startup=on_startup)
    logger.warning("Polling stopped. Goodbye!")
