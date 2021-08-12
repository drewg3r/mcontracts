import sys
from os import path

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from peewee import SqliteDatabase

from data import config
from utils.rids import load_ids, generate_ids

from loguru import logger

logger.info("Starting bot...")

logger.remove()
logger.add("debug.log", diagnose=False, level="INFO")
logger.add(sys.stderr, diagnose=False)

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


db = SqliteDatabase("contracts.db")
db.connect()


if not path.exists(".ids"):
    generate_ids(".ids", config.MIN_RID, config.MAX_RID)

rid, iid = load_ids(".ids")
