import datetime

import peewee
from loguru import logger

from utils.db_api.models import Contract, Invoice, User, UserToContractConnector
from utils.exceptions import UserNotFoundException
from utils.utils import escape_html_symbols


def create_invoice(telegram_user_id: int, description: str, money_from_creator: bool, amount: int) -> Contract:
    description = escape_html_symbols(description)

    try:
        user = User.get(User.telegram_id == telegram_user_id)
        contract = Contract.create(type=1, status=1, description=description,
                                   date_created=datetime.date.today())
        Invoice.create(contract=contract, sum=amount, money_from_creator=money_from_creator)
        UserToContractConnector.create(user=user, contract=contract, is_creator=True, is_hidden=False)
    except peewee.DoesNotExist:
        logger.error("User with telegram ID {} not found in DB while creating new invoice", telegram_user_id)
        raise UserNotFoundException
    return contract
