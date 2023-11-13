from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton, InlineKeyboardMarkup)

from database.temporary_info import usersdictplaycache


def create_dictionary_keyboard(user_id) -> InlineKeyboardMarkup:
    dct = usersdictplaycache[user_id]
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text="✖", callback_data="close_dct"))
    kb_builder.row(
        *[
            InlineKeyboardButton(text=f"{dct[i][0]}", callback_data=f"answer-{i}")
            for i in range(0, 2)
        ]
    )
    kb_builder.row(
        *[
            InlineKeyboardButton(text=f"{dct[i][0]}", callback_data=f"answer-{i}")
            for i in range(2, 4)
        ]
    )
    return kb_builder.as_markup()


def create_dictionary_answer_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text="✖", callback_data="close_dct"),
        InlineKeyboardButton(text="REPORT", callback_data="report_dct"),
        InlineKeyboardButton(text=">>", callback_data="next_question"),
    )
    return kb_builder.as_markup()



