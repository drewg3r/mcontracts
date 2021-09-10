import peewee
from loguru import logger

from loader import rid, bot
from middlewares import i18n
from services.common import get_telegram_user, generate_user_info
from utils.db_api.models import Contract
from utils.db_api.statuses import InvoiceStatus
from utils.exceptions import ContractNotFoundException, InvalidContractStatusException

_ = i18n.gettext


async def invoice_info(contract_id: int, parties_info: bool = False) -> tuple[dict, Contract]:
    try:
        contract = Contract.get(Contract.id == contract_id)
    except peewee.DoesNotExist:
        logger.error("Cannot generate invoice info: Contract#{} does not exists",
                     contract_id)
        raise ContractNotFoundException

    parties = {}
    for user in contract.users:
        telegram_user = await get_telegram_user(user.user.telegram_id)
        if parties_info:
            parties["creator" if user.is_creator else "signer"] =\
                generate_user_info(telegram_user)
        else:
            parties["creator" if user.is_creator else "signer"] = telegram_user
    if not parties.get("signer"):
        parties["signer"] = _("<i>контракт еще не подписан</i>")

    if contract.status == InvoiceStatus.SignNeeded:
        invoice_status = _("Ожидается подпись")
        invoice_status_emoji = "✍"
    elif contract.status == InvoiceStatus.Active:
        invoice_status = _("Контракт активен")
        invoice_status_emoji = "📄"
    elif contract.status == InvoiceStatus.Done:
        invoice_status = _("Контракт закрыт")
        invoice_status_emoji = "✅"
    else:
        logger.error("Contract#{}: unknown status({})", contract.id,
                     contract.status.status_id())
        raise InvalidContractStatusException

    return {
        "invoice": rid[contract.id],
        "date_created": contract.date_created,
        "creator": parties.get("creator"),
        "signer": parties.get("signer"),
        "direction": _("Автор -> Подписанту") if contract.invoice.money_from_creator else
        _("Подписант -> Автору"),
        "sum": contract.invoice.sum,
        "description": contract.description if contract.description else _("<i>без описания</i>"),
        "status": invoice_status,
        "emoji_status": invoice_status_emoji,
    }, contract


async def generate_invoice_list_body(contract: Contract, from_user_id: int) -> dict:
    parties = []

    if contract.status == InvoiceStatus.SignNeeded:
        direction = _("<i>договор еще не подписан</i>")
    else:
        for party in contract.users:
            parties.append(party.user.telegram_id)

        if not contract.invoice.money_from_creator:
            parties.reverse()

        if parties[0] == from_user_id:
            user_data = await bot.get_chat_member(parties[1], parties[1])
            parties[0] = _("Вы")
            parties[1] = user_data.user.full_name
        else:
            user_data = await bot.get_chat_member(parties[0], parties[0])
            parties[0] = user_data.user.full_name
            parties[1] = _("Вам")

        direction = parties[0] + " -> " + parties[1]

    return {
        "invoice": rid[contract.id],
        "sum": contract.invoice.sum,
        "description": contract.description,
        "direction": direction,
        "date_created": contract.date_created if contract.date_created else "no_date"
    }
