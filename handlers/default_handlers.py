from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.chat_action import ChatActionSender

from database.queries import AsyncQuery
from filters.filters import (IsDelBookmarkCallbackData, IsDigitCallbackData,
                             IsPage, IsRatio, IsTTSBook)
from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON, LEXICON_RU, LEXICON_default
from states.bot_states import FSMStates
from tts.tts import text_to_speech

router = Router()


@router.message(Command(commands=["start"]))
async def process_start_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=f"{LEXICON_RU['greeting']} {message.from_user.first_name}!"
    )
    await message.answer(text=LEXICON_RU["greeting-con"])
    if await AsyncQuery.select_user(message.from_user.id) is None:
        await AsyncQuery.insert_user(message.from_user.id, message.from_user.first_name)


@router.message(Command(commands=["help"]), StateFilter(FSMStates.play_dict))
async def process_help_dictionary(message: Message):
    await message.answer(LEXICON_default["help"])


@router.message(Command(commands=["cancel"]), StateFilter(default_state))
async def process_cancel_message(message: Message):
    await message.answer(text=f"Пока нечего отменять, {message.from_user.first_name}")


@router.message(Command(commands=["Cancel"]), StateFilter(default_state))
async def process_cancel_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=f"Возврат к начальной области команд")


@router.message(Command(commands=["my_info"]), StateFilter(default_state))
async def process_cancel_message(message: Message):
    user = await AsyncQuery.select_user(message.from_user.id)
    await message.answer(
        text=f"Ваш прогресс:\n"
        f"Всего ответов: {user.answers}\n"
        f"Правильные ответы: {user.right_answers}\n"
        f"Неверные ответы: {user.wrong_answers}"
    )


@router.message(Command(commands=["read_book", "continue"]))
async def process_read_book_default_state(message: Message, state: FSMContext):
    await state.set_state(FSMStates.reading_book)
    page = await AsyncQuery.select_user_book_page(message.from_user.id)
    tpl_page = await AsyncQuery.select_book_page(page)
    await message.answer(
        text=tpl_page[0], reply_markup=create_pagination_keyboard(page, tpl_page[1])
    )


# Этот хэндлер будет срабатывать на команду "/bookmarks"
# и отправлять пользователю список сохраненных закладок,
# если они есть или сообщение о том, что закладок нет
@router.message(Command(commands="bookmarks"))
async def process_bookmarks_command(message: Message, state: FSMContext):
    await state.set_state(FSMStates.bookmarks_list)
    bmarks = await AsyncQuery.select_users_bookmarks(message.from_user.id)
    if bmarks:
        pages = [bmark.page for bmark in bmarks]
        snippets = await AsyncQuery.select_book_page(pages)
        dct = {i.page_id: i.page_text[:40] for i in snippets}
        await message.answer(
            text=LEXICON[message.text], reply_markup=create_bookmarks_keyboard(dct)
        )
    else:
        await message.answer(text=LEXICON["no_bookmarks"])
