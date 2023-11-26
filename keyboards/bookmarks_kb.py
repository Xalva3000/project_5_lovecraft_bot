from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON_bookmarks


def create_bookmarks_keyboard(dct) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания

    for button in sorted(dct):
        kb_builder.row(
            InlineKeyboardButton(
                text=f"{button} - {dct[button]}",
                callback_data=str(button)
            )
        )
    # Добавляем в клавиатуру в конце две кнопки "Редактировать" и "Отменить"
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_bookmarks["edit_bookmarks_button"],
            callback_data="edit_bookmarks"
        ),
        InlineKeyboardButton(text=LEXICON_bookmarks["menu"],
                             callback_data="cancel_bookmarks"),
        width=2,
    )
    return kb_builder.as_markup()


def create_edit_keyboard(dct) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    nl = '\n'
    # Наполняем клавиатуру кнопками-закладками в порядке возрастания
    for button in sorted(dct):
        kb_builder.row(
            InlineKeyboardButton(
                text=f'{LEXICON_bookmarks["del_button"]} {button} - {dct[button][:12].replace(nl, " ")}',
                callback_data=f"{button}del",
            )
        )
    # Добавляем в конец клавиатуры кнопку "Отменить"
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_bookmarks["cancel_button"],
            callback_data="cancel-bookmarks-edit"
        )
    )
    return kb_builder.as_markup()
