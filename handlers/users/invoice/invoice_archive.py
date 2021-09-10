import peewee
from aiogram.types import CallbackQuery
from loguru import logger

from keyboards.inline.invoice import invoice_share_keyboard
from loader import dp, bot, rid, iid
from middlewares import i18n
from services.invoice.archive import archive_invoice, restore_invoice
from services.invoice.finish import is_finish_available

_ = i18n.gettext


@dp.callback_query_handler(text_contains="invoice_archive")
async def invoice_archive_callback(call: CallbackQuery):
    contract_id = iid[int(call.data.split(":")[1])]

    if archive_invoice(contract_id, call.from_user.id):
        finish_button = is_finish_available(contract_id, call.from_user.id)

        reply_markup = invoice_share_keyboard(rid[contract_id],
                                              finish_button=finish_button,
                                              archive_button=False,
                                              restore_button=True)

        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=reply_markup)
        await call.answer(text=_("Инвойс архивирован"), show_alert=False)
    else:
        await call.answer(text=_("Возникла ошибка"), show_alert=False)


@dp.callback_query_handler(text_contains="invoice_restore")
async def invoice_restore_callback(call: CallbackQuery):
    contract_id = iid[int(call.data.split(":")[1])]

    if restore_invoice(contract_id, call.from_user.id):
        finish_button = is_finish_available(contract_id, call.from_user.id)

        reply_markup = invoice_share_keyboard(rid[contract_id],
                                              finish_button=finish_button,
                                              archive_button=True,
                                              restore_button=False)

        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=reply_markup)
        await call.answer(text=_("Инвойс восстановлен"), show_alert=False)
    else:
        await call.answer(text=_("Возникла ошибка"), show_alert=False)
