from aiogram import Bot
from aiogram.types import CallbackQuery
from loguru import logger

from keyboards.inline.invoice import invoice_refresh_keyboard
from loader import bot, dp
from middlewares import i18n
from services.invoice.info import invoice_info
from services.invoice.sign import sign_invoice
from utils.exceptions import InvalidCallbackDataException, \
    ContractNotFoundException, ContractAlreadySignedException, \
    SigningOwnContractException, UserIsUnregisteredException, \
    InvalidContractIDException
from utils.templates import t

_ = i18n.gettext


@dp.callback_query_handler(text_contains="invoice_sign")
async def sign_invoice_callback(call: CallbackQuery):
    logger.debug("User#{} requested invoice sign", call.from_user.id)
    try:
        contract_id = int(call.data.split(":")[1])
    except (ValueError, IndexError):
        logger.error("Invalid callback data from User#{}", call.from_user.id)
        raise InvalidCallbackDataException

    try:
        contract = sign_invoice(contract_id, call.from_user.id)
    except InvalidContractIDException:
        await call.answer(text=_("Произошла внутренняя ошибка"))
        return
    except ContractNotFoundException:
        await call.answer(text=_("Внутренняя ошибка: контракт не найден"),
                          show_alert=True)
        return
    except ContractAlreadySignedException:
        await call.answer(text=_("Этот контракт уже подписан. "
                                 "Нажмите на кнопку \"Обновить\""))
        return
    except SigningOwnContractException:
        await call.answer(text=_("Вы не можете подписать контракт "
                                 "являясь его автором"))
        return
    except UserIsUnregisteredException:
        _bot = await Bot.get_current().get_me()
        await call.answer(text=_("Для работы с контрактами вы должны нажать "
                                 "кнопку СТАРТ в боте @{}").format(_bot.username),
                          show_alert=True)
        return

    invoice_data, contract = await invoice_info(contract.id, parties_info=True)

    await bot.edit_message_text(inline_message_id=call.inline_message_id,
                                text=_(t["invoice_info"]).format(**invoice_data),
                                reply_markup=invoice_refresh_keyboard(contract_id))
    await call.answer(text=_("Контракт подписан"))
    logger.debug("Invoice signed successfully")
