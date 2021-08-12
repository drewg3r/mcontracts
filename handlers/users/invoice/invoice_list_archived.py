import math

from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from handlers.users.invoice.utils import generate_invoice_info, generate_invoice_list_body
from keyboards.inline.invoice import invoice_paging_keyboard
from loader import dp
from utils.db_api.models import User, UserToContractConnector, Contract
from utils.misc import lang


@dp.message_handler(Command("list_invoices_archived"))
async def list_invoices_archived_handler(message: Message):
    page = 1

    user = User.get(User.telegram_id == message.from_user.id)
    contracts = Contract.select().join(UserToContractConnector).where(UserToContractConnector.user_id == user.id,
                                                                      Contract.type == 1,
                                                                      UserToContractConnector.is_hidden == True) \
        .order_by(Contract.id.desc())

    invoice_list_body = ""

    for contract in contracts[(page - 1) * 3:page * 3]:
        invoice_list_body += await generate_invoice_list_body(contract, message.from_user.id)

    invoice_list_body = invoice_list_body if invoice_list_body else lang.ru["invoice_no_archived_invoices"]
    total_pages = math.ceil(len(contracts) / 3)

    page_contents = lang.ru["invoice_archived_list"] + invoice_list_body
    reply_markup = invoice_paging_keyboard(page - 1, page + 1 if page != total_pages else page,
                                           "{}/{}".format(page, total_pages), is_hidden=True)

    await message.answer(text=page_contents,
                         reply_markup=reply_markup)

