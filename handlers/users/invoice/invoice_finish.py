import peewee
from aiogram.types import CallbackQuery
from loguru import logger

from handlers.users.invoice.utils import generate_invoice_info
from keyboards.inline.invoice import invoice_share_keyboard
from loader import bot, dp, iid, rid
from utils.db_api.models import Contract, UserToContractConnector, User
from utils.misc import lang


@dp.callback_query_handler(text_contains="invoice_finish")
async def invoice_finish_callback(call: CallbackQuery):
    contract_id = iid[int(call.data.split(":")[1])]
    contract = Contract.get(Contract.id == contract_id)

    if finish_invoice(contract, call.from_user.id):

        invoice_info = await generate_invoice_info(contract)

        await bot.edit_message_text(message_id=call.message.message_id,
                                    chat_id=call.message.chat.id,
                                    text=lang.ru["invoice_info"].format(**invoice_info),
                                    reply_markup=invoice_share_keyboard(rid[contract.id]))
        await call.answer(text=lang.ru["invoice_finish_done_alert"], show_alert=False)
    else:
        await call.answer(text=lang.ru["common_error"], show_alert=False)


def finish_invoice(contract, telegram_user_id):
    if len(contract.users) == 1:
        logger.error("Invoice#{} is not signed", contract.id)
        return False

    if contract.users[contract.invoice.money_from_creator].user.telegram_id != telegram_user_id:
        logger.error("Someone(not receiver) trying to finish Invoice#{}", contract.id)
        return False

    try:
        for user in contract.users:
            utcc = UserToContractConnector.get(UserToContractConnector.user_id == user.user.id,
                                               UserToContractConnector.contract_id == contract.id)
            utcc.is_hidden = True
            utcc.save()

        contract.status = 3
        contract.save()
    except peewee.DoesNotExist:
        logger.error("Can't get UserToContractConnector: DoesNotExist")
    except Exception as err:
        logger.opt(exception=err).error("Broad Exception")

    logger.debug("User#{} finished Invoice#{}", telegram_user_id, contract.id)
    return True
