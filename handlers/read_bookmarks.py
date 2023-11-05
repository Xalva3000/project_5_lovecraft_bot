from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, FSInputFile, Message

from database.queries import AsyncQuery
from filters.filters import (IsDelBookmarkCallbackData, IsDigitCallbackData)
from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON, LEXICON_RU
from states.bot_states import FSMStates
from tts.tts import text_to_speech

router = Router()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "отменить" во время работы со списком закладок (просмотр и редактирование)
@router.callback_query(F.data == "cancel_bookmarks")
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(text=LEXICON["cancel_text"])
    await callback.answer()


@router.callback_query(F.data == "cancel-bookmarks-edit")
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.bookmarks_list)
    bmarks = await AsyncQuery.select_users_bookmarks(callback.from_user.id)
    if bmarks:
        pages = [bmark.page for bmark in bmarks]
        snippets = await AsyncQuery.select_book_page(pages)
        dct = {i.page_id: i.page_text[:40] for i in snippets}
        await callback.message.edit_text(
            text=LEXICON["/bookmarks"], reply_markup=create_bookmarks_keyboard(dct)
        )
    else:
        await callback.answer(text=LEXICON["no_bookmarks"])


@router.message(
    Command(commands=["cancel", "отмена"]), StateFilter(FSMStates.bookmarks_list)
)
async def process_cancel_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=LEXICON["cancel_text"])


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок
@router.callback_query(IsDigitCallbackData(), StateFilter(FSMStates.bookmarks_list))
async def process_bookmark_press(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.reading_book)
    tpl_text = await AsyncQuery.select_book_page(int(callback.data))
    await AsyncQuery.update_users_book_page(callback.from_user.id, int(callback.data))
    await callback.message.edit_text(
        text=tpl_text[0],
        reply_markup=create_pagination_keyboard(int(callback.data), tpl_text[1]),
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@router.callback_query(F.data == "edit_bookmarks")
async def process_edit_press(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.edit_bookmarks)
    bmarks = await AsyncQuery.select_users_bookmarks(callback.from_user.id)
    if bmarks:
        pages = [bmark.page for bmark in bmarks]
        snippets = await AsyncQuery.select_book_page(pages)
        dct = {i.page_id: i.page_text[:40] for i in snippets}
    await callback.message.edit_text(
        text=LEXICON[callback.data], reply_markup=create_edit_keyboard(dct)
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
@router.callback_query(
    IsDelBookmarkCallbackData(), StateFilter(FSMStates.edit_bookmarks)
)
async def process_del_bookmark_press(callback: CallbackQuery):
    await AsyncQuery.delete_users_bookmark(
        callback.from_user.id, int(callback.data[:-3])
    )
    bmarks = await AsyncQuery.select_users_bookmarks(callback.from_user.id)
    if bmarks:
        pages = [bmark.page for bmark in bmarks]
        snippets = await AsyncQuery.select_book_page(pages)
        dct = {i.page_id: i.page_text[:40] for i in snippets}
        await callback.message.edit_text(
            text=LEXICON["/bookmarks"], reply_markup=create_edit_keyboard(dct)
        )
    else:
        await callback.message.edit_text(text=LEXICON["no_bookmarks"])
    await callback.answer()
