from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_pagination_keyboard(page: int | str, max_page: int) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками
    kb_builder.row(
        *[
            InlineKeyboardButton(text="<<", callback_data="backward"),
            InlineKeyboardButton(text=f"{page}/{max_page}", callback_data=f"{page}/{max_page}"),
            InlineKeyboardButton(text="✖", callback_data="close_book"),
            InlineKeyboardButton(
                text=f"🔊 {page}", callback_data=f"voice-{page}"
            ),
            InlineKeyboardButton(text=">>", callback_data="forward"),
        ]
    )
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()
