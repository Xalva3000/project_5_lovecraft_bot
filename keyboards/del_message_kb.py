from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton, InlineKeyboardMarkup)


def create_del_message_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text="✖", callback_data="del_message"))
    return kb_builder.as_markup()

def create_del_audio_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text="✖", callback_data="del_audio"))
    return kb_builder.as_markup()
