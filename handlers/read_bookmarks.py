from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.queries import AsyncQuery
from filters.filters import (IsDelBookmarkCallbackData, IsDigitCallbackData)
from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards.return_menu_kb import create_return_menu_keyboard
from keyboards.pagination_kb import create_pagination_keyboard
from keyboards.del_message_kb import create_del_message_keyboard
from lexicon.lexicon import LEXICON_bookmarks
from states.bot_states import FSMStates

router = Router()


@router.message(Command(commands='help'), FSMStates.bookmarks_list)
async def process_bookmarks_help_message(message: Message):
    await message.answer(text=LEXICON_bookmarks['help'],
                         reply_markup=create_del_message_keyboard())


@router.callback_query(F.data == "cancel-bookmarks-edit")
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.bookmarks_list)
    pages = await AsyncQuery.select_users_bookmarks(callback.from_user.id)
    if pages:
        snippets = await AsyncQuery.select_book_page(pages)
        dct = {i.page_id: i.page_text[:12].replace('\n', ' ') for i in snippets}
        await callback.message.edit_text(
            text=LEXICON_bookmarks["/bookmarks"],
            reply_markup=create_bookmarks_keyboard(dct)
        )
    else:
        await callback.answer(text=LEXICON_bookmarks["no_bookmarks"])


@router.message(
    Command(commands=["cancel"]), StateFilter(FSMStates.bookmarks_list)
)
async def process_cancel_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=LEXICON_bookmarks["cancel_text"])


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок
@router.callback_query(IsDigitCallbackData(), StateFilter(FSMStates.bookmarks_list))
async def process_bookmark_press(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.reading_book)
    max_page = await AsyncQuery.select_max_book_page()
    page_text = await AsyncQuery.select_book_page(int(callback.data))
    await AsyncQuery.update_users_book_page(callback.from_user.id, int(callback.data))
    await callback.message.edit_text(
        text=page_text,
        reply_markup=create_pagination_keyboard(int(callback.data), max_page),
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@router.callback_query(F.data == "edit_bookmarks")
async def process_edit_press(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.edit_bookmarks)
    pages = await AsyncQuery.select_users_bookmarks(callback.from_user.id)
    if pages:
        snippets = await AsyncQuery.select_book_page(pages)
        dct = {i.page_id: i.page_text[:12].replace('\n', ' ') for i in snippets}
    await callback.message.edit_text(
        text=LEXICON_bookmarks[callback.data],
        reply_markup=create_edit_keyboard(dct)
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
@router.callback_query(
    IsDelBookmarkCallbackData(),
    StateFilter(FSMStates.edit_bookmarks)
)
async def process_del_bookmark_press(callback: CallbackQuery):
    await AsyncQuery.delete_users_bookmark(
        callback.from_user.id,
        int(callback.data[:-3])
    )
    pages = await AsyncQuery.select_users_bookmarks(callback.from_user.id)
    if pages:
        snippets = await AsyncQuery.select_book_page(pages)
        dct = {i.page_id: i.page_text[:12].replace('\n', ' ') for i in snippets}
        await callback.message.edit_text(
            text=LEXICON_bookmarks["/bookmarks"],
            reply_markup=create_edit_keyboard(dct)
        )
    else:
        await callback.message.edit_text(
            text=LEXICON_bookmarks["no_bookmarks"],
            reply_markup=create_return_menu_keyboard()
        )
    await callback.answer()
