from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.chat_action import ChatActionSender

from database.queries import AsyncQuery
from filters.filters import IsPage, IsChapter, IsRatio, IsTTSBook
from keyboards.return_menu_kb import create_return_menu_keyboard
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON_reading_book, LEXICON_bookmarks
from states.bot_states import FSMStates
from tts.tts import text_to_speech_book
from os import listdir
router = Router()


@router.message(Command(commands=["help"]), StateFilter(FSMStates.reading_book))
async def process_help_reading_book_command(message: Message):
    await message.answer(text=LEXICON_reading_book["help"])


@router.message(Command(commands=["read_book", "continue"]))
async def process_read_book_default_state(message: Message, state: FSMContext):
    await state.set_state(FSMStates.reading_book)
    page = await AsyncQuery.select_user_book_page(message.from_user.id)
    tpl_page = await AsyncQuery.select_book_page(page)
    await message.answer(
        text=tpl_page[0], reply_markup=create_pagination_keyboard(page, tpl_page[1])
    )


# Хендлер отмены
@router.message(
    Command(commands=["cancel"]), StateFilter(FSMStates.reading_book)
)
async def process_cancel_message(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_reading_book["cancel"])
    await state.clear()


# Хендлер срабатывает на строку типа '/стр {page_num}'
# парсит номер страницы, собирает информацию страницы из ДБ
# передает текст страницы и клавиатуру чтения книги
@router.message(IsPage())
async def process_bookmark_press(message: Message, state: FSMContext) -> None:
    await state.set_state(FSMStates.reading_book)
    page = int(message.text.replace("/стр ", ""))
    await AsyncQuery.update_users_book_page(message.from_user.id, page)
    tpl_page = await AsyncQuery.select_book_page(page)
    await message.answer(
        text=tpl_page[0], reply_markup=create_pagination_keyboard(page, tpl_page[1])
    )


@router.message(IsChapter())
async def process_open_page_where_chapter_id(message: Message, state: FSMContext) -> None:
    chapter_id = int(message.text.replace("/фраг ", ""))
    await state.set_state(FSMStates.reading_book)
    page = await AsyncQuery.select_page_of_chapter(chapter_id)
    await AsyncQuery.update_users_book_page(message.from_user.id, page)
    tpl_page = await AsyncQuery.select_book_page(page)
    await message.answer(
        text=tpl_page[0], reply_markup=create_pagination_keyboard(page, tpl_page[1])
    )


# Хендлер нажатия кнопки вперед
@router.callback_query(F.data == "forward")
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.reading_book)
    user = await AsyncQuery.select_user(callback.from_user.id)
    if user.current_mn_page < 251:
        tpl_text = await AsyncQuery.select_book_page(user.current_mn_page + 1)
        await AsyncQuery.update_users_book_page(callback.from_user.id, "forward")
        await callback.message.edit_text(
            text=tpl_text[0],
            reply_markup=create_pagination_keyboard(
                user.current_mn_page + 1, tpl_text[1]
            ),
        )
    elif user.current_mn_page >= 251:
        tpl_text = await AsyncQuery.select_book_page(0)
        await AsyncQuery.update_users_book_page(callback.from_user.id, 0)
        await callback.message.edit_text(
            text=tpl_text[0], reply_markup=create_pagination_keyboard(0, 0)
        )
    await callback.answer()


# Хэндлер нажатия кнопки 'назад'
@router.callback_query(F.data == "backward")
async def process_backward_press(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.reading_book)
    user = await AsyncQuery.select_user(callback.from_user.id)
    if user.current_mn_page in range(1, 252):
        tpl_text = await AsyncQuery.select_book_page(user.current_mn_page - 1)
        await AsyncQuery.update_users_book_page(callback.from_user.id, "backward")
        await callback.message.edit_text(
            text=tpl_text[0],
            reply_markup=create_pagination_keyboard(
                user.current_mn_page - 1, tpl_text[1]
            ),
        )
    await callback.answer()


# Хэндлер нажатия инлайн-кнопки "добавить в закладки",
# с номером текущей страницы и добавлять текущую страницу в закладки
@router.callback_query(IsRatio())
async def process_page_press(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.reading_book)
    all_pages = await AsyncQuery.select_users_bookmarks(callback.from_user.id)
    if len(all_pages) <= 10:
        page = await AsyncQuery.select_user_book_page(callback.from_user.id)
        await AsyncQuery.insert_bookmark(callback.from_user.id, page)
        await callback.answer(LEXICON_bookmarks["add_bookmark"])
    else:
        await callback.answer(LEXICON_bookmarks["bookmark_limit"])


# Хендлер срабатывает на нажатие кнопки озвучивания фрагмента,
# принимая callback строку вида 'voice-{page_num}'
@router.callback_query(IsTTSBook(), StateFilter(FSMStates.reading_book))
async def process_voice_book(callback: CallbackQuery, bot: Bot):
    fragment_id = callback.data.replace("voice-", "")
    text = await AsyncQuery.select_book_fragment(int(fragment_id))

    if fragment_id + '-tts.mp3' not in listdir('tts/book/'):
        await text_to_speech_book(text, int(fragment_id))

    audio = FSInputFile(
        path=f"tts/book/{fragment_id}-tts.mp3", filename=f"{text[:13]}.mp3"
    )
    async with ChatActionSender.upload_document(chat_id=callback.message.chat.id):
        await bot.send_audio(callback.message.chat.id,
                             audio=audio)
