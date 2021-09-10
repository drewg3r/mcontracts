from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from keyboards.inline.invoice import invoice_paging_keyboard
from loader import dp
from middlewares import i18n
from services.invoice.paginator import get_page
from utils.templates import t

_ = i18n.gettext


@dp.message_handler(Command("list_archived"))
async def list_invoices_archived_handler(message: Message):
    page_data = await get_page(message.from_user.id, 0, archived=True)
    invoice_list_body = ""

    for invoice in page_data.page_body:
        invoice_list_body += _(t["list_invoice_body"]).format(**invoice)

    invoice_list_body = invoice_list_body if invoice_list_body else _("\n\nУ вас нет архивных инвойсов")

    reply_header = _("<b>Список архивных инвойсов</b>")

    reply_text = reply_header + invoice_list_body
    reply_markup = invoice_paging_keyboard(page_data.prev_page, page_data.next_page,
                                           "{}/{}".format(page_data.current_page+1 if page_data.page_body else 0,
                                                          page_data.total_pages),
                                           is_hidden=True)

    await message.answer(text=reply_text,
                         reply_markup=reply_markup)
