from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified
from loguru import logger

from keyboards.inline.invoice import invoice_share_keyboard, invoice_sign_keyboard, invoice_refresh_keyboard
from loader import dp, bot, iid, rid
from middlewares import i18n
from services.invoice.archive import is_invoice_archived
from services.invoice.finish import is_finish_available
from utils.db_api.statuses import InvoiceStatus
from utils.templates import t
from services.invoice.info import invoice_info

_ = i18n.gettext


@dp.callback_query_handler(text_contains="invoice_refresh_inline")
async def invoice_refresh_inline_callback(call: CallbackQuery):
    try:
        contract_id = iid[int(call.data.split(":")[1])]
    except (KeyError, ValueError):
        logger.error("Invalid callback data")
        return

    invoice_data, contract = await invoice_info(contract_id, parties_info=True)

    if contract.status == InvoiceStatus.SignNeeded:
        reply_markup = invoice_sign_keyboard(rid[contract_id])
    else:
        reply_markup = invoice_refresh_keyboard(rid[contract_id])
    try:
        await bot.edit_message_text(inline_message_id=call.inline_message_id,
                                    text=_(t["invoice_info"]).format(**invoice_data),
                                    reply_markup=reply_markup)
    except MessageNotModified:
        pass
    await call.answer(text=_("Информация обновлена"), show_alert=False)


@dp.callback_query_handler(text_contains="invoice_refresh")
async def invoice_refresh_callback(call: CallbackQuery):
    contract_id = iid[int(call.data.split(":")[1])]

    invoice_data, contract = await invoice_info(contract_id, parties_info=True)
    finish_button = is_finish_available(contract_id, call.from_user.id)

    if contract.status == InvoiceStatus.Done:
        archive_available = False
        restore_available = False
    else:
        archive_available = is_invoice_archived(contract_id, call.from_user.id)
        restore_available = not archive_available

    reply_markup = invoice_share_keyboard(rid[contract_id],
                                          finish_button=finish_button,
                                          archive_button=archive_available,
                                          restore_button=restore_available)
    try:
        await bot.edit_message_text(message_id=call.message.message_id,
                                    chat_id=call.message.chat.id,
                                    text=_(t["invoice_info"]).format(**invoice_data),
                                    reply_markup=reply_markup)
    except MessageNotModified:
        pass
    await call.answer(text=_("Информация обновлена"), show_alert=False)
