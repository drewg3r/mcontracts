from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("new_invoice", "Создать новый счёт"),
            types.BotCommand("list_invoices", "Показать список инвойсов"),
            types.BotCommand("list_invoices_archived", "Показать список архивных инвойсов"),
        ]
    )
