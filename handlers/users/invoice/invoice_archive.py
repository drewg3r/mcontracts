import peewee
from aiogram.types import CallbackQuery
from loguru import logger

from handlers.users.invoice.utils import is_finish_available
from keyboards.inline.invoice import invoice_share_keyboard
from loader import dp, bot, rid, iid
from utils.db_api.models import Contract, User, UserToContractConnector
from utils.misc import lang


@dp.callback_query_handler(text_contains="invoice_archive")
async def invoice_archive_callback(call: CallbackQuery):
    contract_id = iid[int(call.data.split(":")[1])]

    contract = Contract.get(Contract.id == contract_id)
    user = User.get(User.telegram_id == call.from_user.id)

    if archive_invoice(contract, user, archive=True):
        finish_button = is_finish_available(contract, user)

        reply_markup = invoice_share_keyboard(rid[contract.id],
                                              finish_button=finish_button,
                                              archive_button=False,
                                              restore_button=True)

        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=reply_markup)
        await call.answer(text=lang.ru["invoice_archived_alert"], show_alert=False)
    else:
        await call.answer(text=lang.ru["common_error"], show_alert=False)


@dp.callback_query_handler(text_contains="invoice_restore")
async def invoice_restore_callback(call: CallbackQuery):
    contract_id = iid[int(call.data.split(":")[1])]

    contract = Contract.get(Contract.id == contract_id)
    user = User.get(User.telegram_id == call.from_user.id)

    if archive_invoice(contract, user, archive=False):
        finish_button = is_finish_available(contract, user)

        reply_markup = invoice_share_keyboard(rid[contract.id],
                                              finish_button=finish_button,
                                              archive_button=True,
                                              restore_button=False)

        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=reply_markup)
        await call.answer(text=lang.ru["invoice_restored_alert"], show_alert=False)
    else:
        await call.answer(text=lang.ru["common_error"], show_alert=False)


def archive_invoice(contract: Contract, user: User, archive: bool = True) -> bool:
    try:
        uttc = UserToContractConnector.get(UserToContractConnector.user_id == user,
                                           UserToContractConnector.contract_id == contract.id)
        uttc.is_hidden = archive
        uttc.save()
    except peewee.DoesNotExist:
        logger.error("User/contract with provided id does not exists in database")
    except Exception as err:
        logger.opt(exception=err).error("Broad Exception")
    else:
        logger.debug("User#{} {} Invoice#{}", user.telegram_id, "archived" if archive else "restored", contract.id)
        return True

    return False
