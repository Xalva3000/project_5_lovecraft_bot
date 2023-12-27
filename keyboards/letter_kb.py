from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton, InlineKeyboardMarkup)


def create_letter_keyboard(letter_id) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text="EDIT", callback_data=f"edit_letter"),
        InlineKeyboardButton(text="✖", callback_data="close_letter"),
    )
    kb_builder.row(
        InlineKeyboardButton(text="<<", callback_data=f"prev_letter_{letter_id}"),
        InlineKeyboardButton(text=f"🔊 {letter_id}", callback_data=f"voice-letter-{letter_id}"),
        InlineKeyboardButton(text=">>", callback_data=f"next_letter_{letter_id}"),
    )
    return kb_builder.as_markup()


