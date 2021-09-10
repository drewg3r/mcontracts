from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline.lang import choose_language_markup
from loader import dp, bot
from middlewares import i18n
from services.common import change_user_locale

_ = i18n.gettext


@dp.message_handler(Command("lang"))
async def change_lang(message: Message):
    await message.answer(
        text=_("Выберите язык"),
        reply_markup=choose_language_markup()
    )


@dp.callback_query_handler(text_contains="change_lang")
async def change_lang_callback_handler(call: CallbackQuery):
    try:
        new_lang = call.data.split(":")[1]
    except IndexError:
        raise IndexError("Incorrect callback data: 1 argument expected (0 given)")

    new_lang = new_lang if new_lang in ["en", "ru", "uk"] else "en"
    change_user_locale(call.from_user.id, new_lang)

    await bot.edit_message_text(message_id=call.message.message_id,
                                chat_id=call.message.chat.id,
                                text=_("Ваш язык изменен"),
                                reply_markup=None)


