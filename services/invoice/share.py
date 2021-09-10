import peewee
from loguru import logger

from services.common import is_contract_signed
from utils.db_api.models import Contract
from utils.exceptions import ContractNotFoundException, ContractAccessDeniedException


def share_invoice(contract_id: int, telegram_user_id: int) -> tuple[Contract, bool]:
    try:
        contract = Contract.get(Contract.id == contract_id)
    except peewee.DoesNotExist:
        logger.error("Contract#{} was not found")
        raise ContractNotFoundException

    if telegram_user_id not in [user.user.telegram_id for user in contract.users]:
        logger.error("User#{} trying to share Contract#{} he does not have access to", telegram_user_id, contract_id)
        raise ContractAccessDeniedException

    return contract, is_contract_signed(contract)
