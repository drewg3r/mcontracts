import peewee
from loguru import logger

from loader import iid
from utils.db_api.models import Contract, User, UserToContractConnector
from utils.exceptions import ContractNotFoundException, ContractAlreadySignedException, SigningOwnContractException, \
    UserIsUnregisteredException, InvalidContractIDException


def sign_invoice(contract_id: int, telegram_user_id: int) -> Contract:
    try:
        contract_id = iid[contract_id]
    except KeyError:
        logger.error("Invalid contract_id{{}) - not found in iid", contract_id)
        raise InvalidContractIDException

    try:
        contract = Contract.get(Contract.id == contract_id)
    except peewee.DoesNotExist:
        logger.error("Contract#{} not found while signing", contract_id)
        raise ContractNotFoundException

    if len(contract.users) > 1:
        logger.error("Contract#{}: signing requested by UID:{}, but contract is already signed",
                     contract_id, telegram_user_id)
        raise ContractAlreadySignedException

    if contract.users[0].user.telegram_id == telegram_user_id:
        logger.debug("Contract#{}: creator trying to sign his own contract", contract_id)
        raise SigningOwnContractException

    try:
        user = User.get(User.telegram_id == telegram_user_id)
    except peewee.DoesNotExist:
        logger.debug("Unregistered User#{} trying to sign an Invoice#{}",
                     telegram_user_id, contract_id)
        raise UserIsUnregisteredException

    UserToContractConnector.create(user=user, contract=contract, is_creator=False, is_hidden=False)
    contract.status = 2
    contract.save()

    return contract
