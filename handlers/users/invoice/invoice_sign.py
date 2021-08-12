import peewee
from aiogram.types import CallbackQuery
from loguru import logger

from handlers.users.invoice.utils import generate_invoice_info
from keyboards.inline.invoice import invoice_refresh_keyboard
from loader import bot, dp, iid, rid
from utils.db_api.models import Contract, UserToContractConnector, User
from utils.misc import lang


@dp.callback_query_handler(text_contains="invoice_sign")
async def test_inline_handler(call: CallbackQuery):
    try:
        contract_id = iid[int(call.data.split(":")[1])]
        contract = Contract.get(Contract.id == contract_id)

        if len(contract.users) > 1:
            await call.answer(text=lang.ru["invoice_sign_error_already_signed"], show_alert=True)
            raise Exception("Contract is already signed")
        if contract.users[0].user.telegram_id == call.from_user.id:
            await call.answer(text=lang.ru["invoice_sign_error_user_is_creator"], show_alert=True)
            raise Exception("Creator is trying to sign own contract")

        try:
            user = User.get(User.telegram_id == call.from_user.id)
        except peewee.DoesNotExist:
            logger.warning("Unregistered User#{} trying to sign an Invoice#{}", call.from_user.id, contract.id)
            await call.answer(text=lang.ru["invoice_sign_error_user_not_registered"], show_alert=True)
            return

        UserToContractConnector.create(user=user, contract=contract, is_creator=False, is_hidden=False)
        contract.status = 2
        contract.save()

        invoice_info = await generate_invoice_info(contract)

        await bot.edit_message_text(inline_message_id=call.inline_message_id,
                                    text=lang.ru["invoice_info"].format(**invoice_info),
                                    reply_markup=invoice_refresh_keyboard(rid[contract_id]))
        await call.answer(text=lang.ru["invoice_sign_done"], show_alert=False)
    except Exception as e:
        print("signing error occurred")
        print(e)
