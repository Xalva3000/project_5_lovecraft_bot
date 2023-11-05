from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton, InlineKeyboardMarkup)


def create_rating_keyboard(excerpt_id) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(text="👎", callback_data=f"down_{excerpt_id}"),
        InlineKeyboardButton(
            text="REPORT", callback_data=f"report_excerpt_{excerpt_id}"
        ),
        InlineKeyboardButton(text="✖", callback_data="close_excerpts"),
        InlineKeyboardButton(
            text=f"🔊 {excerpt_id}", callback_data=f"voice-excerpt-{excerpt_id}"
        ),
        InlineKeyboardButton(text="👍", callback_data=f"up_{excerpt_id}"),
    )
    return kb_builder.as_markup()
