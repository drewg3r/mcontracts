import math
from collections import namedtuple

from services.common import get_user
from services.invoice.info import generate_invoice_list_body
from utils.db_api.models import User, Contract, UserToContractConnector
from utils.exceptions import PageOutOfBoundsException

Page = namedtuple("Page", ["current_page", "next_page", "prev_page", "total_pages", "page_body"])


async def _get_contracts(user: User, archived: bool) -> list[Contract]:
    return Contract.select() \
        .join(UserToContractConnector) \
        .where(
            UserToContractConnector.user_id == user.id,
            Contract.type == 1,
            UserToContractConnector.is_hidden == archived) \
        .order_by(Contract.id.desc())


async def _generate_page_body(telegram_user_id: int, contracts: list[Contract], page: int) -> list[dict]:
    page_body = []
    for contract in contracts[page*3:(page+1)*3]:
        page_body.append(await generate_invoice_list_body(contract, telegram_user_id))
    return page_body


async def get_page(telegram_user_id: int, page: int, archived: bool) -> Page:
    user = get_user(telegram_user_id)

    contracts = await _get_contracts(user, archived=archived)
    max_page = math.ceil(len(contracts) / 3)

    if page < 0 or page > max_page:
        raise PageOutOfBoundsException

    page_body = await _generate_page_body(telegram_user_id, contracts, page)

    return Page(
        current_page=page,
        next_page=0 if not page_body else page+1 if page != max_page-1 else max_page-1,
        prev_page=0 if not page_body else page-1 if page != 0 else 0,
        total_pages=max_page,
        page_body=page_body)
