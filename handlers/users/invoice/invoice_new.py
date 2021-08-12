import peewee
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
import datetime

from loguru import logger

from handlers.users.invoice.utils import generate_invoice_info
from keyboards.default.invoice import new_invoice_markup
from keyboards.inline.invoice import invoice_share_keyboard
from loader import dp, rid
from states.invoice import NewInvoiceStates
from utils.db_api.models import Contract, Invoice, UserToContractConnector, User
from utils.misc import lang


@dp.message_handler(Command("cancel"), state="*")
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(lang.ru["new_invoice_canceled"], reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Command("new_invoice"))
async def new_invoice(message: Message):
    await message.answer(text=lang.ru["new_invoice_create"], reply_markup=new_invoice_markup)
    await NewInvoiceStates.first()


@dp.message_handler(state=NewInvoiceStates.enter_receiver)
async def enter_receiver(message: Message, state: FSMContext):
    if message.text in [lang.ru["new_invoice_keyboard_receive"], lang.ru["new_invoice_keyboard_give"]]:
        await state.update_data(receiver=message.text)
        await message.answer(lang.ru["new_invoice_enter_sum"], reply_markup=ReplyKeyboardRemove())
        await NewInvoiceStates.next()
    else:
        await message.answer(lang.ru["new_invoice_error"])


@dp.message_handler(state=NewInvoiceStates.enter_sum)
async def enter_sum(message: Message, state: FSMContext):
    if len(message.text) <= 12:
        await state.update_data(sum=message.text)
        await message.answer(lang.ru["new_invoice_enter_description"])
        await NewInvoiceStates.next()
    else:
        await message.answer(lang.ru["new_invoice_error"])


@dp.message_handler(state=NewInvoiceStates.enter_description)
async def enter_sum(message: Message, state: FSMContext):
    if len(message.text) <= 64:
        if message.text == "/skip":
            message.text = lang.ru["no_description"]
        await state.update_data(description=message.text)

        contract = await create_invoice(message.from_user.id, state)
        if contract:
            invoice_info = await generate_invoice_info(contract, lang.ru["invoice_info_share"])
            await message.answer(text=lang.ru["invoice_info"].format(**invoice_info),
                                 reply_markup=invoice_share_keyboard(rid[contract.id]))
            await state.finish()
        else:
            await message.answer(lang.ru["new_invoice_error"])
    else:
        await message.answer(lang.ru["new_invoice_error"])


async def create_invoice(telegram_user_id, state):
    try:
        state_data = await state.get_data()

        money_from_creator = True if state_data["receiver"] == lang.ru["new_invoice_keyboard_give"] else False

        contract = Contract.create(type=1, status=1, description=state_data["description"],
                                   date_created=datetime.date.today())

        Invoice.create(contract=contract, sum=state_data["sum"], money_from_creator=money_from_creator)
        user = User.get(User.telegram_id == telegram_user_id)
        UserToContractConnector.create(user=user, contract=contract, is_creator=True, is_hidden=False)
    except peewee.DoesNotExist:
        logger.error("User with provided telegram id does not exists in database")
    except KeyError:
        logger.error("Invalid state's data")
    except Exception as err:
        logger.opt(exception=err).error("Broad Exception")
    else:
        logger.debug("User #{} created Invoice#{}({})", telegram_user_id, contract.id, rid[contract.id])
        return contract

    return None
