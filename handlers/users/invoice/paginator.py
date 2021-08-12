import math

from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from handlers.users.invoice.utils import generate_invoice_info, generate_invoice_list_body
from keyboards.inline.invoice import invoice_paging_keyboard
from loader import dp, bot
from utils.db_api.models import User, UserToContractConnector, Contract
from utils.misc import lang


@dp.callback_query_handler(text_contains="invoice_list_paginator")
async def paginator(call: CallbackQuery):
    try:
        data = call.data.split(":")
        is_hidden = True if data[2] == "True" else False
        page = int(data[1])
        page = page if page > 0 else 1

        user = User.get(User.telegram_id == call.from_user.id)
        contracts = Contract.select().join(UserToContractConnector).where(UserToContractConnector.user_id == user.id,
                                                                          Contract.type == 1,
                                                                          UserToContractConnector.is_hidden == is_hidden) \
            .order_by(Contract.id.desc())

        invoice_list_body = ""

        for contract in contracts[(page - 1) * 3:page * 3]:
            invoice_list_body += await generate_invoice_list_body(contract, call.from_user.id)

        total_pages = math.ceil(len(contracts) / 3)

        if not invoice_list_body:
            invoice_list_body = lang.ru["invoice_no_active_invoices"] if not is_hidden else lang.ru["invoice_no_archived_invoices"]
            reply_markup = invoice_paging_keyboard(1, 1, "0/0", is_hidden=is_hidden)
        else:
            reply_markup = invoice_paging_keyboard(page - 1, page + 1 if page != total_pages else page,
                                                   "{}/{}".format(page, total_pages), is_hidden=is_hidden)

        page_header = lang.ru["invoice_active_list"] if not is_hidden else lang.ru["invoice_archived_list"]
        page_contents = page_header + invoice_list_body

        await bot.edit_message_text(message_id=call.message.message_id,
                                    chat_id=call.message.chat.id,
                                    text=page_contents,
                                    reply_markup=reply_markup)
    except MessageNotModified:
        pass
    finally:
        await call.answer()
