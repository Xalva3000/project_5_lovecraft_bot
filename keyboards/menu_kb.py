from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton, InlineKeyboardMarkup)
from lexicon.lexicon import LEXICON_menu


def create_menu_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(InlineKeyboardButton(text=LEXICON_menu["/read_book"], callback_data="/read_book"))
    kb_builder.row(InlineKeyboardButton(text=LEXICON_menu["/bookmarks"], callback_data="/bookmarks"))
    kb_builder.row(InlineKeyboardButton(text=LEXICON_menu["/read_excerpt"], callback_data="/read_excerpt"),
                   InlineKeyboardButton(text=LEXICON_menu["/add_excerpt"], callback_data="/add_excerpt"))
    kb_builder.row(InlineKeyboardButton(text=LEXICON_menu["/read_letter"], callback_data="/read_letter"),
                   InlineKeyboardButton(text=LEXICON_menu["/add_letter"], callback_data="/add_letter"))
    kb_builder.row(InlineKeyboardButton(text=LEXICON_menu["/play_dict"], callback_data="/play_dict"),
                   InlineKeyboardButton(text=LEXICON_menu["/add_term"], callback_data="/add_term"))
    kb_builder.row(InlineKeyboardButton(text=LEXICON_menu["/my_info"], callback_data="/my_info"),
                   InlineKeyboardButton(text=LEXICON_menu["/urls"], callback_data="/urls"))
    kb_builder.row(InlineKeyboardButton(text="✖", callback_data="close_menu"))
    return kb_builder.as_markup()
