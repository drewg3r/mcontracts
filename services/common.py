import peewee
from aiogram.types import User
from aiogram.utils.exceptions import ChatNotFound
from loguru import logger

from loader import bot
from utils.db_api import models
from utils.db_api.models import Contract
from utils.exceptions import UserIsUnregisteredException, UserNotFoundException, ContractNotFoundException


def get_contract_parties(contract: Contract) -> dict:
    creator = contract.users[0].user
    try:
        signer = contract.users[1].user
    except IndexError:
        signer = None
    return {"creator": creator, "signer": signer}


def is_contract_signed(contract: Contract) -> bool:
    return get_contract_parties(contract)["signer"] is not None


async def get_telegram_user(telegram_user_id: int) -> User:
    try:
        telegram_user = await bot.get_chat_member(telegram_user_id, telegram_user_id)
    except ChatNotFound:
        logger.error("Cannot get telegram User#{}: unregistered", telegram_user_id)
        raise UserIsUnregisteredException
    else:
        return telegram_user.user


def generate_user_info(user: User) -> str:
    if user.username:
        return "{}(@{}), UID: {}".format(user.full_name, user.username, user.id)
    else:
        return "{}, UID: {}".format(user.full_name, user.id)


def get_user(telegram_user_id: int) -> models.User:
    try:
        user = models.User.get(models.User.telegram_id == telegram_user_id)
    except peewee.DoesNotExist:
        logger.error("User#{} does not exists", telegram_user_id)
        raise UserNotFoundException
    return user


def get_contract(contract_id: int) -> Contract:
    try:
        contract = Contract.get(Contract.id == contract_id)
    except peewee.DoesNotExist:
        logger.error("Contract#{} does not exists", contract_id)
        raise ContractNotFoundException
    return contract


def change_user_locale(telegram_user_id: int, locale: str):
    user = get_user(telegram_user_id)
    user.locale = locale
    user.save()
