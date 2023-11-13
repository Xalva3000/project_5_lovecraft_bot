from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.temporary_info import usertextcache
from keyboards.bookmarks_kb import create_bookmarks_keyboard
from keyboards.dictionary_kb import create_dictionary_keyboard
from keyboards.menu_kb import create_menu_keyboard
from keyboards.pagination_kb import create_pagination_keyboard
from keyboards.rating_kb import create_rating_keyboard
from keyboards.topexcerpts_kb import create_topexcerpts_keyboard
from lexicon.lexicon import LEXICON_dict, LEXICON_default, LEXICON_excerpts, LEXICON_bookmarks
from services.cashing import load_answers, load_top_excerpts
from states.bot_states import FSMStates
from database.queries import AsyncQuery


router = Router()


@router.message(Command(commands=["menu"]))
async def process_menu_message(message: Message, state: FSMContext) -> None:
    await state.clear()
    user = await AsyncQuery.select_user(message.from_user.id)
    await message.answer(
        text=f"<b>{user.name}</b> (🍪{user.answers}):",
        reply_markup=create_menu_keyboard()
    )


@router.callback_query(F.data == '/read_book')
async def process_read_book_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.reading_book)
    page = await AsyncQuery.select_user_book_page(callback.from_user.id)
    tpl_page = await AsyncQuery.select_book_page(page)
    await callback.message.edit_text(
        text=tpl_page[0], reply_markup=create_pagination_keyboard(page, tpl_page[1])
    )


@router.callback_query(F.data == "/play_dict")
async def process_play_dictionary_button(callback: CallbackQuery, state: FSMContext):
    """Хендлер команды /play_dict. Загрузка определение из БД, если терминов в словаре достаточно,
    то устанавливается состояние игры Словарь, и собирается клавиатура из вариантов ответов."""
    text = await load_answers(callback.from_user.id)
    if text is None:
        await callback.message.edit_text(text=LEXICON_dict["need_more_terms"])
    else:
        await state.set_state(FSMStates.play_dict)
        await callback.message.edit_text(
            text=text, reply_markup=create_dictionary_keyboard(callback.from_user.id)
        )


@router.callback_query(F.data == "/add_term")
async def process_add_term_button(callback: CallbackQuery, state: FSMContext):
    """Хендлер команды /add_term. Устанавливает состояние добавление термина.
    Сообщает о том, что нужно вводить термин и в каком виде."""
    await state.set_state(FSMStates.adding_term)
    await callback.message.edit_text(text=LEXICON_dict["add_term"])


@router.callback_query(F.data == "/bookmarks")
async def process_bookmarks_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.bookmarks_list)
    pages = await AsyncQuery.select_users_bookmarks(callback.from_user.id)
    if pages:
        snippets = await AsyncQuery.select_book_page(pages)
        dct = {i.page_id: i.page_text[:40] for i in snippets}
        await callback.message.edit_text(
            text=LEXICON_bookmarks[callback.data], reply_markup=create_bookmarks_keyboard(dct)
        )
    else:
        await callback.message.edit_text(text=LEXICON_bookmarks["no_bookmarks"])


@router.callback_query(F.data == "/random_excerpt")
async def process_random_excerpt_button(callback: CallbackQuery, state: FSMContext):
    # запрос кортежа (текст, порядковый номер, имя добавившего)
    tpl_text = await AsyncQuery.select_random_excerpt()
    if tpl_text:
        await state.set_state(FSMStates.reading_excerpts)
        await callback.message.edit_text(
            text=tpl_text[0] + f'\n\n{LEXICON_excerpts["added_by"]} {tpl_text[2]}',
            reply_markup=create_rating_keyboard(tpl_text[1]))
    else:
        await callback.message.edit_text(
            text=LEXICON_excerpts["no_excerpts"])


@router.callback_query(F.data == "/read_top_excerpts")
async def process_read_excerpts_button(callback: CallbackQuery, state: FSMContext):
    await load_top_excerpts()
    if usertextcache:
        await state.set_state(FSMStates.reading_excerpts)
        await callback.message.edit_text(
            text=usertextcache[0], reply_markup=create_topexcerpts_keyboard(0)
        )
    else:
        await callback.message.edit_text(text=LEXICON_excerpts["no_excerpts"])


@router.callback_query(F.data == "/add_excerpt")
async def process_offer_excerpt_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.adding_excerpt)
    await callback.message.edit_text(text=LEXICON_excerpts["add_excerpt"])


@router.callback_query(F.data == "/my_info")
async def process_info_button(callback: CallbackQuery) -> None:
    """Хендлер команды /my_info. Присылает сообщение с данными статистики пользователя
    в игре 'Словарь'"""
    user = await AsyncQuery.select_user(callback.from_user.id)
    tpl = LEXICON_default["my_info"]
    await callback.message.edit_text(
        text=f"{tpl[0]}\n"
        f"{tpl[1]} {user.answers}\n"
        f"{tpl[2]} {user.right_answers}\n"
        f"{tpl[3]} {user.wrong_answers}"
    )


@router.callback_query(F.data == '/urls')
async def process_urls_button(callback: CallbackQuery) -> None:
    """Хендлер команды /urls. Присылает сообщение с указанием ссылок
    на полезные ресурсы по тематике бота"""
    await callback.message.edit_text(text=LEXICON_default['urls'])


