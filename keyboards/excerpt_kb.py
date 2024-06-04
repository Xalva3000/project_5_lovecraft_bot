from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton, InlineKeyboardMarkup)


def create_excerpt_keyboard(excerpt_id) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text="EDIT", callback_data=f"edit_excerpt_{excerpt_id}"),
        InlineKeyboardButton(text="✖", callback_data="close_excerpts"),
    )
    kb_builder.row(
        InlineKeyboardButton(text="<<", callback_data=f"prev_excerpt_{excerpt_id}"),
        InlineKeyboardButton(text=f"🔊 {excerpt_id}", callback_data=f"voice-excerpt-{excerpt_id}"),
        InlineKeyboardButton(text=">>", callback_data=f"next_excerpt_{excerpt_id}"),
    )
    return kb_builder.as_markup()
