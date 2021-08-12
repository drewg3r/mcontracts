import json
import os


def get_translations(rootdir: str):
    lang = {}
    lang["general"] = load_json("{}/general.json".format(rootdir))

    lang["ru"] = {}
    lang["ru"]["inv"] = load_json(rootdir+"/ru/common.json")
    print(lang)


def load_json(filename: str):
    with open(filename, "r") as f:
        data = json.load(f)
    return data


ru = {
    "/start": "Добро пожаловать, {name}!\nВведите /help для получения справки",
    "/help": "Этот бот позволяет создавать договорённости. Сейчас доступна только договорённость типа «счёт».\nДля её "
             "создания введите /new_invoice",
    "new_invoice_create": "Создаём новый инвойс.\nВы хотите получить или отдать деньги?\n(/cancel - отмена)",
    "new_invoice_keyboard_receive": "👛Получить",
    "new_invoice_keyboard_give": "💸Отдать",
    "new_invoice_enter_sum": "Теперь введите сумму",
    "new_invoice_enter_description": "Отлично. Теперь введите описание\n(/skip - пропустить)",
    "new_invoice_created": "Инвойс создан! Отправьте другу для подписи",
    "invoice_share": "Поделиться",
    "invoice_sign": "🤝Подписать",
    "new_invoice_error": "Ошибка. Введите данные еще раз или отмените создание счёта(/cancel)",
    "new_invoice_canceled": "Отменено",
    "invoice_share_label": "Поделиться договором №{invoice}",
    "invoice_info": "{emoji_status}<b>Счёт №{invoice}</b>\n<b>Статус:</b> {status}\n\n<b>Автор:</b> {"
                    "creator}\n<b>Подписант:</b> {signer}\n\nДоговор о "
                    "передаче денег:\n{direction}\n\n<b>Сумма:</b> {sum}\n\n<b>Дата создания:</b> {date_created}\n\n<b>Описание:</b> {"
                    "description}\n\n\n{additional_info}",
    "invoice_direction_cts": "Автор -> Подписанту",
    "invoice_direction_stc": "Подписант -> Автору",
    "invoice_info_no_signer": "<i>договор еще не подписан</i>",
    "invoice_info_share": "",
    "invoice_info_sign": "",
    "invoice_inline_send": "Отправить договор №{invoice}",
    "invoice_status_sign": "Ожидается подпись",
    "invoice_status_active": "Контракт активен",
    "invoice_status_done": "Контракт закрыт",
    "invoice_sign_error_user_not_registered": "Вы должны отправить боту команду /start прежде чем начать пользоваться "
                                              "контрактами",
    "invoice_sign_error_user_is_creator": "Вы не можете подписать контракт являясь его автором",
    "invoice_sign_error_already_signed": "Этот контракт уже подписан!",
    "invoice_sign_done": "Вы подписали контракт",
    "invoice_active_list": "<b>Список активных инвойсов:</b>",
    "invoice_archived_list": "<b>Список архивных инвойсов:</b>",
    "invoice_active_body": "\n\n<b>Инвойс №{invoice}</b>\n<b>Сумма:</b> {sum}\n<b>Описание:</b> {description}\n{direction}\n{date_created}\n<b>Подробнее:</b> /inv_info_{invoice}\n",
    "invoice_finish_button": "Закрыть",
    "invoice_no_active_invoices": "\nУ вас нет активных инвойсов",
    "invoice_no_archived_invoices": "\nУ вас нет архивных инвойсов",
    "invoice_finish_error_not_receiver": "Вы должны быть получателем денег чтоб закрыть контракт",
    "invoice_finish_error_not_signed": "Контракт еще не подписан",
    "invoice_finish_done_alert": "Контракт был закрыт",
    "invoice_button_refresh": "🔄Обновить",
    "invoice_refresh_alert": "Информация обновлена",
    "invoice_button_archive": "📥Архивировать",
    "invoice_button_restore": "📤Восстановить",
    "invoice_archived_alert": "Инвойс архивирован",
    "invoice_restored_alert": "Инвойс восстановлен",
    "no_description": "<i>без описания</i>",
    "you": "вам",
    "You": "Вы",
    "common_error": "Возникла ошибка"
}

# get_translations("../../data/translations")
