from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.queries import AsyncQuery
from database.temporary_info import usersdictplaycache
from filters.filters import IsAnswer, IsDictPattern
from keyboards.dictionary_kb import (create_dictionary_answer_keyboard,
                                     create_dictionary_keyboard)
from lexicon.lexicon import LEXICON_dict
from states.bot_states import FSMStates
from services.cashing import load_answers

router = Router()


@router.message(Command(commands=["help"]), StateFilter(FSMStates.play_dict))
async def process_help_dictionary(message: Message):
    """Хендлер команды /help при состоянии игры 'Словарь'."""
    await message.answer(LEXICON_dict["help"])


@router.message(Command(commands=["cancel"]), StateFilter(FSMStates.play_dict))
async def process_dictionary_cancel(message: Message, state: FSMContext):
    """Хендлер команды /cancel. Отмена состояния игры 'Словарь'."""
    await state.clear()
    await message.answer(text=LEXICON_dict["cancel"])


@router.message(Command(commands=["play_dict"]))
async def process_play_dictionary(message: Message, state: FSMContext):
    """Хендлер команды /play_dict. Загрузка определение из БД, если терминов в словаре достаточно,
    то устанавливается состояние игры Словарь, и собирается клавиатура из вариантов ответов."""
    text = await load_answers(message.from_user.id)
    if text is None:
        await message.answer(text=LEXICON_dict["need_more_terms"])
    else:
        await state.set_state(FSMStates.play_dict)
        await message.answer(
            text=text, reply_markup=create_dictionary_keyboard(message.from_user.id)
        )


@router.callback_query(F.data == "close_dct")
async def process_close_dict_button(callback: CallbackQuery, state: FSMContext):
    """Хендлер завершения игры по кнопке закрытия.
    Сброс состояния, удаление сообщения и клавиатуры."""
    await state.clear()
    await callback.message.delete_reply_markup()
    await callback.message.delete()


@router.callback_query(F.data == "next_question")
async def process_next_button(callback: CallbackQuery, state: FSMContext):
    """Хендлер кнопки '>>'. Загрузка новых определений в кэш,
    и сборка новой клавиатуры из вариантов ответов."""
    await state.set_state(FSMStates.play_dict)
    user_id = callback.from_user.id
    text = await load_answers(user_id)
    await callback.message.edit_text(
        text=text, reply_markup=create_dictionary_keyboard(user_id)
    )


@router.callback_query(IsAnswer())
async def process_dictionary_answer(callback: CallbackQuery, state: FSMContext):
    """Обработка ответа на тест игры 'Словарь'. Обновляет соответствующие значения в БД, в таблице users,
    в зависимости от ответа. И сборка нового вопроса."""
    await state.set_state(FSMStates.play_dict)
    user_id = callback.from_user.id
    dct = usersdictplaycache[user_id]
    answer = int(callback.data.replace("answer-", ""))
    if usersdictplaycache[user_id][answer][1] == "wrong":
        await callback.answer(text=LEXICON_dict["user_wrong_answer"])
        await AsyncQuery.update_users_wrong_answer(user_id)
    elif usersdictplaycache[user_id][answer][1] == "right":
        await callback.answer(text=LEXICON_dict["user_right_answer"])
        await AsyncQuery.update_users_right_answer(user_id)
    text = (
        f"<b>{LEXICON_dict['system_right_answer'][0]}</b>\n{dct['current_data'][0]}"
        f"\n\n<b>{LEXICON_dict['system_right_answer'][1]}</b>\n{dct['current_data'][1]}"
        f"\n\n<b>{LEXICON_dict['system_right_answer'][2]}</b>\n{dct['current_data'][2]}"
    )
    await callback.message.edit_text(
        text=text, reply_markup=create_dictionary_answer_keyboard()
    )


@router.callback_query(F.data == "report_dct")
async def process_report_button(callback: CallbackQuery):
    """Хендлер кнопки REPORT при игре 'Словарь'.
    Кэш всего составленного вопроса отправляется в БД.
    Выводится сообщение, что вопрос отправлен на проверку"""
    await AsyncQuery.insert_questionable_dct(callback.from_user.id)
    await callback.answer(text=LEXICON_dict["report"])


@router.message(Command(commands=["add_term"]))
async def process_add_term_message(message: Message, state: FSMContext):
    """Хендлер команды /add_term. Устанавливает состояние добавление термина.
    Сообщает о том, что нужно вводить термин и в каком виде."""
    await state.set_state(FSMStates.adding_term)
    await message.answer(text=LEXICON_dict["add_term"])


@router.message(Command(commands=["cancel"]), StateFilter(FSMStates.adding_term))
async def process_add_term_cancel(message: Message, state: FSMContext):
    """Хедлер команды /cancel при состоянии добавления термина.
    Сброс состояния добавления термина. Сообщение об отмене."""
    await state.clear()
    await message.answer(text=LEXICON_dict["add_cancel"])


@router.message(IsDictPattern(), StateFilter(FSMStates.adding_term))
async def process_insert_user_term(message: Message, state: FSMContext):
    """Хедлер принятия пользовательского термина. Если введенное пользователем
    сообщение соответствует шаблону новых терминов, то термин добавляется в БД,
    и выводится сообщение об успешно добавлении"""
    await state.clear()
    term_tpl = tuple(message.text.split("$$"))
    await AsyncQuery.insert_term(term_tpl)
    await message.answer(text=LEXICON_dict["add_success"])


@router.message(Command(commands=["reset_stats"]), StateFilter(FSMStates.play_dict))
async def process_reset_stats_message(message: Message):
    """Хендлер команды /reset_stats.
    Обнуление статистики пользователя в БД таблице users."""
    await AsyncQuery.reset_users_stats(message.from_user.id)
    await message.answer(text=LEXICON_dict["reset_stats"])
