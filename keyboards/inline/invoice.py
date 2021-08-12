from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.misc import lang


def invoice_share_keyboard(switch_inline_query, finish_button=False, archive_button=False, restore_button=False):
    buttons = [
        [
            InlineKeyboardButton(text=lang.ru["invoice_button_refresh"],
                                 callback_data="invoice_refresh:{}".format(switch_inline_query)),
        ],
        [
            InlineKeyboardButton(text=lang.ru["invoice_share"],
                                 switch_inline_query=str(switch_inline_query))
        ]
    ]

    if finish_button:
        buttons[0].append(InlineKeyboardButton(text=lang.ru["invoice_finish_button"],
                                               callback_data="invoice_finish:{}".format(switch_inline_query)))

    if archive_button:
        buttons.insert(1, [InlineKeyboardButton(text=lang.ru["invoice_button_archive"],
                                                callback_data="invoice_archive:{}".format(switch_inline_query))])

    if restore_button:
        buttons.insert(1, [InlineKeyboardButton(text=lang.ru["invoice_button_restore"],
                                                callback_data="invoice_restore:{}".format(switch_inline_query))])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def invoice_sign_keyboard(callback_data):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=lang.ru["invoice_button_refresh"],
                                 callback_data="invoice_refresh_inline:{}".format(callback_data)),
        ], [
            InlineKeyboardButton(text=lang.ru["invoice_sign"], callback_data="invoice_sign:{}".format(callback_data))
        ]
    ])


def invoice_refresh_keyboard(callback_data):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=lang.ru["invoice_button_refresh"],
                                 callback_data="invoice_refresh_inline:{}".format(callback_data)),
        ]
    ])


def invoice_paging_keyboard(left: int, right: int, middle_text: str, is_hidden: bool = False) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅", callback_data="invoice_list_paginator:{}:{}".format(left, is_hidden)),
            InlineKeyboardButton(text=middle_text, callback_data="invoice_list_paginator:0:{}".format(is_hidden)),
            InlineKeyboardButton(text="➡", callback_data="invoice_list_paginator:{}:{}".format(right, is_hidden)),
        ]
    ])
