from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton, InlineKeyboardMarkup)


def create_topexcerpts_keyboard(excerpt_pos) -> InlineKeyboardMarkup:
    pos, name_pos = excerpt_pos, excerpt_pos + 1
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        *[
            InlineKeyboardButton(text="✖", callback_data="close_top_excerpts"),
            InlineKeyboardButton(
                text=f"🔊 {name_pos}", callback_data=f"voice-top-excerpt-{pos}"
            ),
            InlineKeyboardButton(text=">>", callback_data=f"next_{pos}"),
        ]
    )
    return kb_builder.as_markup()
