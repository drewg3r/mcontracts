from aiogram.types import Message

from handlers.users.invoice.utils import generate_invoice_info, is_finish_available, is_invoice_archived
from keyboards.inline.invoice import invoice_share_keyboard
from loader import dp, iid, rid
from utils.db_api.models import Contract, User
from utils.misc import lang


@dp.message_handler(text_contains="/inv_info_")
async def invoice_info_handler(message: Message):
    try:
        contract_id = iid[int(message.text.split("/inv_info_")[1])]
        contract = Contract.get(Contract.id == contract_id)
        user = User.get(User.telegram_id == message.from_user.id)

        invoice_info = await generate_invoice_info(contract)
        answer_text = lang.ru["invoice_info"].format(**invoice_info)
        finish_button = is_finish_available(contract, user)
        is_archived = is_invoice_archived(contract, user)

        reply_markup = invoice_share_keyboard(rid[contract_id],
                                              finish_button=finish_button,
                                              archive_button=not is_archived,
                                              restore_button=is_archived)

        await message.answer(text=answer_text, reply_markup=reply_markup)
    except Exception as e:
        print(e)
