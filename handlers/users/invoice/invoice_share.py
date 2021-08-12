import hashlib

from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from loguru import logger

from handlers.users.invoice.utils import generate_invoice_info
from keyboards.inline.invoice import invoice_sign_keyboard
from loader import dp, bot, iid, rid
from utils.db_api.models import Contract
from utils.misc import lang


@dp.inline_handler()
async def inline_share(inline_query: InlineQuery):
    text = inline_query.query or 'none'
    if text == "none":
        return

    try:
        contract = Contract.get(Contract.id == iid[int(text)])

        if inline_query.from_user.id not in [user.user.telegram_id for user in contract.users]:
            raise Exception("User not in contract's users")

        invoice_info = await generate_invoice_info(contract, lang.ru["invoice_info_sign"])
        if invoice_info["signer"] != lang.ru["invoice_info_no_signer"]:
            invoice_info["additional_info"] = ""
            signer_set = True
        else:
            signer_set = False

        input_content = InputTextMessageContent(lang.ru["invoice_info"].format(**invoice_info))
        result_id: str = hashlib.md5(text.encode()).hexdigest()
        item = InlineQueryResultArticle(
            id=result_id,
            title=lang.ru["invoice_inline_send"].format(**invoice_info),
            input_message_content=input_content,
            reply_markup=invoice_sign_keyboard(rid[contract.id]) if not signer_set else None
        )
        await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)
    except Exception as err:
        logger.opt(exception=err).error("Broad Exception")

