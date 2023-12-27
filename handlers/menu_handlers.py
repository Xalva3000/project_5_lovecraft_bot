from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.bookmarks_kb import create_bookmarks_keyboard
from keyboards.dictionary_kb import create_dictionary_keyboard
from keyboards.letter_kb import create_letter_keyboard
from keyboards.menu_kb import create_menu_keyboard
from keyboards.pagination_kb import create_pagination_keyboard
from keyboards.excerpt_kb import create_excerpt_keyboard
from keyboards.return_menu_kb import create_return_menu_keyboard
from lexicon.lexicon import LEXICON_dict, LEXICON_default, LEXICON_excerpts, LEXICON_bookmarks, LEXICON_letters
from services.cashing import load_answers
from states.bot_states import FSMStates
from database.queries import AsyncQuery
from filters.filters import IsAdmin


router = Router()


@router.message(Command(commands=["menu"]))
async def process_menu_message(message: Message, state: FSMContext) -> None:
    """Хендлер сообщения /menu. Выводит клавиатуру интерактивного меню."""
    await state.clear()
    user = await AsyncQuery.select_user(message.from_user.id)
    await message.answer(
        text=f"<b>{user.name}</b> (🍪{user.answers}):",
        reply_markup=create_menu_keyboard()
    )


@router.callback_query(F.data == 'close_menu')
async def process_close_menu_button(callback: CallbackQuery, state: FSMContext):
    """Хендлер кнопки закрытия клавиатуры интерактивного меню."""
    await state.clear()
    await callback.message.delete_reply_markup()
    await callback.message.delete()


@router.callback_query(F.data == '/read_book')
async def process_read_book_button(callback: CallbackQuery, state: FSMContext):
    """Хендлер кнопки чтения книги. Вывод страницы книги пользователя,
    указанной в БД и клавиатуры пагинации"""
    await state.set_state(FSMStates.reading_book)
    page = await AsyncQuery.select_user_book_page(callback.from_user.id)
    tpl_page = await AsyncQuery.select_book_page(page)
    await callback.message.edit_text(
        text=tpl_page[0], reply_markup=create_pagination_keyboard(page, tpl_page[1])
    )


@router.callback_query(F.data == "/play_dict")
async def process_play_dictionary_button(callback: CallbackQuery, state: FSMContext):
    """Хендлер кнопки игры 'Словарь'. Загрузка определение из БД, если терминов в словаре достаточно,
    то устанавливается состояние игры Словарь, и собирается клавиатура из вариантов ответов."""
    text = await load_answers(callback.from_user.id)
    if text is None:
        await callback.message.edit_text(text=LEXICON_dict["need_more_terms"],
                                         reply_markup=create_return_menu_keyboard())
    else:
        await state.set_state(FSMStates.play_dict)
        await callback.message.edit_text(
            text=text, reply_markup=create_dictionary_keyboard(callback.from_user.id)
        )


@router.callback_query(F.data == "/add_term")
async def process_add_term_button(callback: CallbackQuery, state: FSMContext):
    """Хендлер кнопки добавить термин. Устанавливает состояние добавление термина.
    Сообщает о том, что нужно вводить термин и в каком виде."""
    await state.set_state(FSMStates.adding_term)
    await callback.message.edit_text(text=LEXICON_dict["add_term"],
                                     reply_markup=create_return_menu_keyboard())


@router.callback_query(F.data == "/bookmarks")
async def process_bookmarks_button(callback: CallbackQuery, state: FSMContext):
    """Хендлер кнопки добавить термин. Устанавливает состояние добавление термина.
        Сообщает о том, что нужно вводить термин и в каком виде."""
    await state.set_state(FSMStates.bookmarks_list)
    pages = await AsyncQuery.select_users_bookmarks(callback.from_user.id)
    if pages:
        snippets = await AsyncQuery.select_book_page(pages)
        dct = {i.page_id: i.page_text[:12].replace('\n', ' ') for i in snippets}
        await callback.message.edit_text(
            text=LEXICON_bookmarks[callback.data],
            reply_markup=create_bookmarks_keyboard(dct)
        )
    else:
        await callback.message.edit_text(text=LEXICON_bookmarks["no_bookmarks"],
                                         reply_markup=create_return_menu_keyboard())


@router.callback_query(F.data == "/random_excerpt")
async def process_random_excerpt_button(callback: CallbackQuery, state: FSMContext):
    """Хендлер кнопки случайного отрывка"""
    # запрос кортежа (текст, порядковый номер, имя добавившего)
    tpl_text = await AsyncQuery.select_random_excerpt()
    if tpl_text:
        await state.set_state(FSMStates.reading_excerpts)
        await callback.message.edit_text(
            text=tpl_text[0] + f'\n\n{LEXICON_excerpts["added_by"]} {tpl_text[2]}',
            reply_markup=create_excerpt_keyboard(tpl_text[1]))
    else:
        await callback.message.edit_text(
            text=LEXICON_excerpts["no_excerpts"],
            reply_markup=create_return_menu_keyboard()
        )


@router.callback_query(F.data == "/add_excerpt")
async def process_offer_excerpt_button(callback: CallbackQuery, state: FSMContext):
    """Хендлер кнопки добавления отрывка"""
    await state.set_state(FSMStates.adding_excerpt)
    await callback.message.edit_text(text=LEXICON_excerpts["add_excerpt"],
                                     reply_markup=create_return_menu_keyboard())


@router.callback_query(F.data == "/read_letter")
async def process_first_letter_button(callback: CallbackQuery, state: FSMContext):
    """Хендлер кнопки письма"""
    current_letter_id = await AsyncQuery.select_user_current_letter(callback.from_user.id)
    # запрос кортежа (текст, порядковый номер, имя добавившего)
    letter = await AsyncQuery.select_letter(current_letter_id)
    if letter:
        await state.set_state(FSMStates.reading_letters)
        await callback.message.edit_text(
            text=letter.letter + f'\n\n{LEXICON_letters["added_by"]} {letter.user_name}',
            reply_markup=create_letter_keyboard(letter_id=letter.id))
    else:
        await callback.message.edit_text(
            text=LEXICON_letters["no_letters"],
            reply_markup=create_return_menu_keyboard()
        )


@router.callback_query(F.data == "/add_letter")
async def process_offer_letter_button(callback: CallbackQuery, state: FSMContext):
    """Хендлер кнопки добавления письма"""
    await state.set_state(FSMStates.adding_letter)
    await callback.message.edit_text(text=LEXICON_letters["add_letter"],
                                     reply_markup=create_return_menu_keyboard())


@router.callback_query(F.data == "/my_info")
async def process_info_button(callback: CallbackQuery) -> None:
    """Хендлер кнопки /my_info. Выводит данные статистики пользователя
    в игре 'Словарь'"""
    user = await AsyncQuery.select_user(callback.from_user.id)
    tpl = LEXICON_default["my_info"]
    await callback.message.edit_text(
        text=f"{tpl[0]}\n\n"
        f"{tpl[1]} {user.answers}\n\n"
        f"{tpl[2]} {user.right_answers}\n"
        f"{tpl[3]} {user.wrong_answers}",
        reply_markup=create_return_menu_keyboard()
    )


@router.callback_query(F.data == '/urls')
async def process_urls_button(callback: CallbackQuery) -> None:
    """Хендлер кнопки /urls. Присылает сообщение с указанием ссылок
    на полезные ресурсы по тематике бота"""
    await callback.message.edit_text(
        text=LEXICON_default['urls'],
        reply_markup=create_return_menu_keyboard())
