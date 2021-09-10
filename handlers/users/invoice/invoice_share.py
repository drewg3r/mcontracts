import hashlib

from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from loguru import logger

from keyboards.inline.invoice import invoice_sign_keyboard
from loader import dp, bot, iid, rid
from middlewares import i18n
from services.invoice.info import invoice_info
from services.invoice.share import share_invoice
from utils.exceptions import ContractNotFoundException, ContractAccessDeniedException
from utils.templates import t

_ = i18n.gettext


@dp.inline_handler()
async def inline_share(inline_query: InlineQuery):
    try:
        contract_id = iid[int(inline_query.query)]
    except (ValueError, KeyError):
        logger.error("Invalid callback data from User#{}",
                     inline_query.from_user.id)
        return

    try:
        contract, is_signed = share_invoice(contract_id, inline_query.from_user.id)
    except ContractNotFoundException:
        logger.warning("User#{} trying to share invalid Contract({})",
                       inline_query.from_user.id, contract_id)
        return
    except ContractAccessDeniedException:
        logger.error("User#{} trying to share contract he doesn't have access to(#{})",
                     inline_query.from_user.id, contract_id)
        return

    invoice_data, contract = await invoice_info(contract.id, parties_info=True)
    input_content = InputTextMessageContent(_(t["invoice_info"]).format(**invoice_data))
    result_id: str = hashlib.md5(inline_query.query.encode()).hexdigest()
    item = InlineQueryResultArticle(
        id=result_id,
        title=_("Отправить контракт №{}").format(rid[contract_id]),
        input_message_content=input_content,
        reply_markup=invoice_sign_keyboard(rid[contract.id]) if not is_signed else None
    )
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)
