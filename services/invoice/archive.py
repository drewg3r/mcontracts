import peewee
from loguru import logger

from services.common import get_contract, get_user
from utils.db_api.models import User, Contract, UserToContractConnector
from utils.exceptions import UserNotFoundException, ContractNotFoundException


def _archive_restore_invoice(contract: Contract, user: User, archive: bool) -> bool:
    try:
        uttc = UserToContractConnector.get(UserToContractConnector.user_id == user,
                                           UserToContractConnector.contract_id == contract.id)
        uttc.is_hidden = archive
        uttc.save()
    except peewee.DoesNotExist:
        logger.error("User/contract with provided id does not exists in database")
    else:
        logger.debug("User#{} archived/restored Invoice#{}".format(
            user.telegram_id, contract.id
        ))
        return True

    return False


def is_invoice_archived(contract_id: int, telegram_user_id: int) -> bool:
    try:
        user = User.get(User.telegram_id == telegram_user_id)
    except peewee.DoesNotExist:
        logger.error("User#{} does not exists", telegram_user_id)
        raise UserNotFoundException
    try:
        contract = Contract.get(Contract.id == contract_id)
    except peewee.DoesNotExist:
        logger.error("Contract#{} does not exists", contract_id)
        raise ContractNotFoundException

    try:
        uttc = UserToContractConnector.get(UserToContractConnector.user_id == user,
                                           UserToContractConnector.contract_id == contract.id)
    except peewee.DoesNotExist:
        logger.error("Can't get UserToContractConnector: DoesNotExist")
    else:
        return uttc.is_hidden


def archive_invoice(contract_id: int, telegram_user_id: int) -> bool:
    contract = get_contract(contract_id)
    user = get_user(telegram_user_id)
    return _archive_restore_invoice(contract, user, archive=True)


def restore_invoice(contract_id: int, telegram_user_id: int) -> bool:
    contract = get_contract(contract_id)
    user = get_user(telegram_user_id)
    return _archive_restore_invoice(contract, user, archive=False)

