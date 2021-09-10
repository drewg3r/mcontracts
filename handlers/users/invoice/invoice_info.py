from aiogram.types import Message

from keyboards.inline.invoice import invoice_share_keyboard
from loader import dp, iid, rid
from middlewares import i18n
from services.invoice.archive import is_invoice_archived
from services.invoice.finish import is_finish_available
from services.invoice.info import invoice_info
from utils.db_api.statuses import InvoiceStatus
from utils.templates import t

_ = i18n.gettext


@dp.message_handler(text_contains="/inv_info_")
async def invoice_info_handler(message: Message):
    contract_id = iid[int(message.text.split("/inv_info_")[1])]

    invoice_data, contract = await invoice_info(contract_id, parties_info=True)
    answer_text = _(t["invoice_info"]).format(**invoice_data)
    finish_button = is_finish_available(contract_id, message.from_user.id)
    if contract.status == InvoiceStatus.Done:
        archive_available = False
        restore_available = False
    else:
        archive_available = is_invoice_archived(contract_id, message.from_user.id)
        restore_available = not archive_available

    reply_markup = invoice_share_keyboard(rid[contract_id],
                                          finish_button=finish_button,
                                          archive_button=archive_available,
                                          restore_button=restore_available)

    await message.answer(text=answer_text, reply_markup=reply_markup)

