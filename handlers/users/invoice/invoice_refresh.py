from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from handlers.users.invoice.utils import generate_invoice_info, is_finish_available, is_invoice_archived
from keyboards.inline.invoice import invoice_share_keyboard, invoice_sign_keyboard, invoice_refresh_keyboard
from loader import dp, bot, iid, rid
from utils.db_api.models import Contract, User
from utils.misc import lang


@dp.callback_query_handler(text_contains="invoice_refresh_inline")
async def invoice_refresh_inline_callback(call: CallbackQuery):
    contract_id = iid[int(call.data.split(":")[1])]
    contract = Contract.get(Contract.id == contract_id)

    invoice_info = await generate_invoice_info(contract)

    if contract.status == 1:
        reply_markup = invoice_sign_keyboard(rid[contract_id])
    else:
        reply_markup = invoice_refresh_keyboard(rid[contract_id])
    try:
        await bot.edit_message_text(inline_message_id=call.inline_message_id,
                                    text=lang.ru["invoice_info"].format(**invoice_info),
                                    reply_markup=reply_markup)
    except MessageNotModified:
        pass
    await call.answer(text=lang.ru["invoice_refresh_alert"], show_alert=False)


@dp.callback_query_handler(text_contains="invoice_refresh")
async def invoice_refresh_callback(call: CallbackQuery):
    contract_id = iid[int(call.data.split(":")[1])]
    contract = Contract.get(Contract.id == contract_id)
    user = User.get(User.telegram_id == call.from_user.id)

    invoice_info = await generate_invoice_info(contract)
    finish_button = is_finish_available(contract, user)
    is_archived = is_invoice_archived(contract, user)

    reply_markup = invoice_share_keyboard(rid[contract_id],
                                          finish_button=finish_button,
                                          archive_button=not is_archived,
                                          restore_button=is_archived)
    try:
        await bot.edit_message_text(message_id=call.message.message_id,
                                    chat_id=call.message.chat.id,
                                    text=lang.ru["invoice_info"].format(**invoice_info),
                                    reply_markup=reply_markup)
    except MessageNotModified:
        pass
    await call.answer(text=lang.ru["invoice_refresh_alert"], show_alert=False)
