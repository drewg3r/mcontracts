from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from keyboards.inline.invoice import invoice_paging_keyboard
from loader import dp, bot
from middlewares import i18n
from services.invoice.paginator import get_page
from utils.templates import t

_ = i18n.gettext


@dp.callback_query_handler(text_contains="invoice_list_paginator")
async def paginator(call: CallbackQuery):
    try:
        data = call.data.split(":")
        is_hidden = True if data[2] == "True" else False
        page = int(data[1])

        page_data = await get_page(call.from_user.id, page, archived=is_hidden)

        invoice_list_body = ""
        for invoice in page_data.page_body:
            invoice_list_body += _(t["list_invoice_body"]).format(**invoice)

        reply_header = _("<b>Список архивных инвойсов</b>") if is_hidden else \
                       _("<b>Список активных инвойсов</b>")

        if not invoice_list_body:
            invoice_list_body = _("\n\nУ вас нет архивных инвойсов") if is_hidden else \
                                _("\n\nУ вас нет актинвых инвойсов")

        reply_text = reply_header + invoice_list_body
        reply_markup = invoice_paging_keyboard(
            left=page_data.prev_page,
            right=page_data.next_page,
            middle_text="{}/{}".format(
                page_data.current_page+1 if page_data.page_body else 0,
                page_data.total_pages),
            is_hidden=is_hidden
        )

        await bot.edit_message_text(message_id=call.message.message_id,
                                    chat_id=call.message.chat.id,
                                    text=reply_text,
                                    reply_markup=reply_markup)
    except MessageNotModified:
        pass
    finally:
        await call.answer()
