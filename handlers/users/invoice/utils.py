import peewee
from loguru import logger

from loader import bot, rid
from utils.db_api.models import Contract, User, UserToContractConnector
from utils.misc import lang


async def generate_invoice_info(contract: Contract, additional_info: str = ""):
    parties = {}
    for user in contract.users:
        user_data = await bot.get_chat_member(user.user.telegram_id, user.user.telegram_id)
        if user_data.user.username:
            user_str = "{}(@{}), UID: {}".format(user_data.user.full_name, user_data.user.username, user_data.user.id)
        else:
            user_str = "{}, UID: {}".format(user_data.user.full_name, user_data.user.id)
        role = "creator" if user.is_creator else "signer"
        parties[role] = user_str

    if contract.status == 1:
        invoice_status = lang.ru["invoice_status_sign"]
        invoice_status_emoji = "✍"
    elif contract.status == 2:
        invoice_status = lang.ru["invoice_status_active"]
        invoice_status_emoji = "📄"
    else:
        invoice_status = lang.ru["invoice_status_done"]
        invoice_status_emoji = "✅"

    return {
        "invoice": rid[contract.id],
        "date_created": contract.date_created if contract.date_created else "no_date",
        "creator": parties["creator"] if "creator" in parties.keys() else "no creator",
        "signer": parties["signer"] if "signer" in parties.keys() else lang.ru["invoice_info_no_signer"],
        "direction": lang.ru["invoice_direction_cts"] if contract.invoice.money_from_creator else lang.ru[
            "invoice_direction_stc"],
        "sum": contract.invoice.sum,
        "description": contract.description,
        "status": invoice_status,
        "emoji_status": invoice_status_emoji,
        "additional_info": additional_info
    }


async def generate_invoice_list_body(contract: Contract, from_user_id: int):
    parties = []

    if contract.status == 1:
        direction = lang.ru["invoice_info_no_signer"]
    else:
        for party in contract.users:
            parties.append(party.user.telegram_id)

        if not contract.invoice.money_from_creator:
            parties.reverse()

        if parties[0] == from_user_id:
            user_data = await bot.get_chat_member(parties[1], parties[1])
            parties[0] = lang.ru["You"]
            parties[1] = user_data.user.full_name
        else:
            user_data = await bot.get_chat_member(parties[0], parties[0])
            parties[0] = user_data.user.full_name
            parties[1] = lang.ru["you"]

        direction = parties[0] + " -> " + parties[1]

    return lang.ru["invoice_active_body"].format(**{
        "invoice": rid[contract.id],
        "sum": contract.invoice.sum,
        "description": contract.description,
        "direction": direction,
        "date_created": contract.date_created if contract.date_created else "no_date"
    })


def is_finish_available(contract: Contract, user: User) -> bool:
    try:
        if contract.users[contract.invoice.money_from_creator].user == user and contract.status == 2:
            return True
    except IndexError:
        return False

    return False


def is_invoice_archived(contract: Contract, user: User) -> bool:
    try:
        uttc = UserToContractConnector.get(UserToContractConnector.user_id == user,
                                           UserToContractConnector.contract_id == contract.id)
    except peewee.DoesNotExist:
        logger.error("Can't get UserToContractConnector: DoesNotExist")
    except Exception as err:
        logger.opt(exception=err).error("Broad Exception")
    else:
        return uttc.is_hidden
