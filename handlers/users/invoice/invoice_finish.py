from aiogram.types import CallbackQuery

from keyboards.inline.invoice import invoice_share_keyboard
from loader import bot, dp, iid, rid
from middlewares import i18n
from services.invoice.finish import finish_invoice
from services.invoice.info import invoice_info
from utils.exceptions import FinishIsNotAvailableException
from utils.templates import t

_ = i18n.gettext


@dp.callback_query_handler(text_contains="invoice_finish")
async def invoice_finish_callback(call: CallbackQuery):
    contract_id = iid[int(call.data.split(":")[1])]

    try:
        contract = finish_invoice(contract_id, call.from_user.id)
    except FinishIsNotAvailableException:
        await call.answer(_("Возникла непредвиденная ошибка"))
        return

    invoice_data, contract = await invoice_info(contract.id, parties_info=True)

    await bot.edit_message_text(message_id=call.message.message_id,
                                chat_id=call.message.chat.id,
                                text=_(t["invoice_info"]).format(**invoice_data),
                                reply_markup=invoice_share_keyboard(rid[contract.id]))
    await call.answer(text=_("Вы закрыли контракт"), show_alert=False)

