from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from loguru import logger

from keyboards.default.invoice import new_invoice_markup
from keyboards.inline.invoice import invoice_share_keyboard
from loader import dp, rid
from middlewares import i18n
from services.invoice.create import create_invoice
from services.invoice.info import invoice_info
from states.invoice import NewInvoiceStates
from utils.exceptions import UserNotFoundException
from utils.templates import t

_ = i18n.gettext


@dp.message_handler(Command("cancel"), state="*")
async def cancel(message: Message, state: FSMContext):
    logger.debug("User#{} cleared his FSM state(/cancel)", message.from_user.id)
    await state.finish()
    await message.answer(_("Отменено"), reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Command("new_invoice"))
async def new_invoice(message: Message):
    logger.debug("User#{} initiated new invoice wizard", message.from_user.id)
    await NewInvoiceStates.first()
    await message.answer(
        text=_("Создаём новый инвойс.\n"
               "Вы хотите получить или отдать деньги?\n"
               "(/cancel - отмена)"),
        reply_markup=new_invoice_markup()
    )


@dp.message_handler(state=NewInvoiceStates.enter_receiver)
async def enter_receiver(message: Message, state: FSMContext):
    if message.text == _("👛Получить"):
        await state.update_data(money_from_creator=False)
        text = _("Теперь введите сумму, которую хотите получить")
    elif message.text == _("💸Отдать"):
        await state.update_data(money_from_creator=True)
        text = _("Теперь введите сумму, которую хотите отдать")
    else:
        logger.debug("User#{} chose invalid option in 'enter receiver' dialog",
                     message.from_user.id)
        text = _("Ошибка. Введите данные еще раз или отмените создание счёта(/cancel)")
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await NewInvoiceStates.next()


@dp.message_handler(state=NewInvoiceStates.enter_sum)
async def enter_sum(message: Message, state: FSMContext):
    if len(message.text) <= 12:
        await state.update_data(sum=message.text)
        await NewInvoiceStates.next()
        text = _("Отлично. Теперь введите описание\n(/skip - пропустить)")
    else:
        logger.debug("User#{} entered invalid invoice sum", message.from_user.id)
        text = _("Ошибка. Введите данные еще раз или отмените"
                 " создание счёта(/cancel)")

    await message.answer(text=text)


@dp.message_handler(state=NewInvoiceStates.enter_description)
async def enter_description(message: Message, state: FSMContext):
    if len(message.text) <= 64:
        if message.text == "/skip":
            message.text = ""

        state_data = await state.get_data()
        try:
            contract = create_invoice(telegram_user_id=message.from_user.id,
                                      description=message.text,
                                      money_from_creator=state_data["money_from_creator"],
                                      amount=state_data["sum"]
                                      )
        except UserNotFoundException:
            await message.answer(_("Вы должны отправить боту команду /start "
                                   "прежде чем начать пользоваться контрактами"))
            return
        finally:
            await state.finish()

        invoice_data, contract = await invoice_info(contract.id, parties_info=True)

        await message.answer(text=_(t["invoice_info"]).format(**invoice_data),
                             reply_markup=invoice_share_keyboard(rid[contract.id]))

    else:
        await message.answer(_("Ошибка. Введите данные еще раз или отмените создание счёта(/cancel)"))
