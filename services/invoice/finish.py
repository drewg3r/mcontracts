import peewee
from loguru import logger

from services.common import get_user, get_contract
from utils.db_api.models import User, Contract, UserToContractConnector
from utils.db_api.statuses import InvoiceStatus
from utils.exceptions import FinishIsNotAvailableException


def _is_finish_available(contract: Contract, user: User) -> bool:
    try:
        if len(contract.users) > 1:
            if contract.users[contract.invoice.money_from_creator].user == user and \
                    contract.status == InvoiceStatus.Active:
                return True
    except IndexError as e:
        logger.error(e)
        return False

    return False


def is_finish_available(contract_id: int, telegram_user_id: int) -> bool:
    user = get_user(telegram_user_id)
    contract = get_contract(contract_id)
    return _is_finish_available(contract, user)


def finish_invoice(contract_id: int, telegram_user_id: int) -> Contract:
    user = get_user(telegram_user_id)
    contract = get_contract(contract_id)

    if _is_finish_available(contract, user):
        try:
            for user in contract.users:
                utcc = UserToContractConnector.get(UserToContractConnector.user_id == user.user.id,
                                                   UserToContractConnector.contract_id == contract.id)
                utcc.is_hidden = True
                utcc.save()

            contract.status = 3
            contract.save()
        except peewee.DoesNotExist:
            logger.error("Can't get UserToContractConnector: DoesNotExist")
    else:
        logger.error("Finish button is not available")
        raise FinishIsNotAvailableException
    logger.debug("User#{} finished Invoice#{}", telegram_user_id, contract.id)
    return contract
