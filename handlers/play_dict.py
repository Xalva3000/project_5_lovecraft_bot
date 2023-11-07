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
    await message.answer(LEXICON_dict["help"])


@router.message(Command(commands=["cancel", "отмена"]))
async def process_dictionary_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=LEXICON_dict["cancel"])


@router.callback_query(F.data == "close_dct")
async def process_close_dict_button(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete_reply_markup()
    await callback.message.delete()


@router.message(Command(commands=["play_dict", "словарь"]))
async def process_play_dictionary(message: Message, state: FSMContext):
    await state.set_state(FSMStates.play_dict)
    text = await load_answers(message.from_user.id)
    await message.answer(
        text=text, reply_markup=create_dictionary_keyboard(message.from_user.id)
    )


@router.callback_query(F.data == "next_question")
async def process_close_dict_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.play_dict)
    user_id = callback.from_user.id
    text = await load_answers(user_id)
    await callback.message.edit_text(
        text=text, reply_markup=create_dictionary_keyboard(user_id)
    )


@router.callback_query(IsAnswer())
async def process_dictionary_answer(callback: CallbackQuery, state: FSMContext):
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
        f"<b>{LEXICON_dict['system_right_answer'][0]}</b>\n{dct['current_data'][0].capitalize()}"
        f"\n\n<b>{LEXICON_dict['system_right_answer'][1]}</b>\n{dct['current_data'][1]}"
    )
    await callback.message.edit_text(
        text=text, reply_markup=create_dictionary_answer_keyboard()
    )


@router.message(Command(commands=["add_term"]))
async def process_add_term(message: Message, state: FSMContext):
    await state.set_state(FSMStates.adding_term)
    await message.answer(text=LEXICON_dict["add_term"])


@router.message(
    Command(commands=["cancel", "отмена"]), StateFilter(FSMStates.adding_term)
)
async def process_dictionary_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=LEXICON_dict["add_cancel"])


@router.message(IsDictPattern(), StateFilter(FSMStates.adding_term))
async def process_add_term(message: Message, state: FSMContext):
    await state.clear()
    term_tpl = tuple(message.text.split("$$"))
    await AsyncQuery.insert_term(term_tpl)
    await message.answer(text=LEXICON_dict["add_success"])


@router.callback_query(F.data == "report_dct")
async def process_report_button(callback: CallbackQuery):
    await AsyncQuery.insert_questionable_dct(callback.from_user.id)
    await callback.answer(text=LEXICON_dict["report"])


@router.message(Command(commands=["reset_stats"]), StateFilter(FSMStates.play_dict))
async def process_cancel_message(message: Message):
    await AsyncQuery.reset_users_stats(message.from_user.id)
    await message.answer(text=LEXICON_dict["reset_stats"])
