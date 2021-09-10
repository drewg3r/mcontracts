from middlewares import i18n

_ = i18n.gettext

t = {
    "invoice_info": "{emoji_status}<b>Счёт №{invoice}</b>\n<b>Статус:</b> {status}\n\n<b>Автор:</b> {"
                      "creator}\n<b>Подписант:</b> {signer}\n\nДоговор о "
                      "передаче денег:\n{direction}\n\n<b>Сумма:</b> {sum}\n\n<b>Дата создания:</b> {"
                      "date_created}\n\n<b>Описание:</b> {description}",

    "list_invoice_body": "\n\n<b>Инвойс №{invoice}</b>\n<b>Сумма:</b> {sum}\n<b>Описание:</b> {description}\n{direction}\n{date_created}\n<b>Подробнее:</b> /inv_info_{invoice}\n",
    "/help": "Этот бот позволяет создавать договорённости. Сейчас доступна только договорённость типа «счёт».\n"
               "Для её создания введите /new_invoice"
}
