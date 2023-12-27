from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.chat_action import ChatActionSender

from database.queries import AsyncQuery
from filters.filters import IsTTSLetter
from keyboards.letter_kb import create_letter_keyboard
from keyboards.return_menu_kb import create_return_menu_keyboard
from keyboards.del_message_kb import create_del_message_keyboard, create_del_audio_keyboard
from states.bot_states import FSMStates
from tts.tts import text_to_speech
from lexicon.lexicon import LEXICON_letters
from services.next_unordered_number import next_unordered_number

router = Router()


@router.message(
    Command(commands=["cancel"]), StateFilter(FSMStates.reading_letters))
async def process_cancel_letter(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_letters["exit_letters"],
                         reply_markup=create_del_message_keyboard())
    await state.clear()


@router.callback_query(IsTTSLetter(), StateFilter(FSMStates.reading_letters))
async def process_voice_letters(callback: CallbackQuery, bot: Bot):
    letter = await AsyncQuery.select_letter(
        int(callback.data.replace("voice-letter-", ""))
    )
    await text_to_speech(letter.letter, callback.from_user.id)
    audio = FSInputFile(
        path=f"tts/{callback.from_user.id}-tts.mp3", filename=f"{letter.letter[:13]}.mp3"
    )
    async with ChatActionSender.upload_document(chat_id=callback.message.chat.id):
        await bot.send_audio(callback.message.chat.id,
                             audio=audio,
                             reply_markup=create_del_audio_keyboard()
                             )


@router.message(StateFilter(FSMStates.adding_letter))
async def process_add_letter(message: Message, state: FSMContext):
    try:
        await AsyncQuery.insert_user_letter(message.text, message.from_user.first_name)
    except Exception as e:
        print(e)
        await message.answer(text=LEXICON_letters["adding_error"],
                             reply_markup=create_del_message_keyboard())
    else:
        await message.answer(text=LEXICON_letters["adding_success"],
                             reply_markup=create_del_message_keyboard())
    finally:
        await state.clear()


@router.callback_query(F.data.startswith('next_letter_'))
async def process_next_letter_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.reading_letters)
    current_letter = int(callback.data.replace('next_letter_', ''))
    all_letter_ids = await AsyncQuery.select_all_letter_ids()

    next_id = next_unordered_number(lst=all_letter_ids, current_number=current_letter)
    next_letter = await AsyncQuery.select_letter(next_id)
    await AsyncQuery.update_user_current_letter(user_id=callback.from_user.id, new_letter_id=next_id)

    if next_letter:
        if next_letter.id == current_letter:
            return await callback.answer(text=LEXICON_letters["only_one_letter"])
        await callback.message.edit_text(
            text=next_letter.letter + f'\n\n{LEXICON_letters["added_by"]} {next_letter.user_name}',
            reply_markup=create_letter_keyboard(next_letter.id),
        )


@router.callback_query(F.data.startswith('prev_letter_'))
async def process_next_letter_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.reading_letters)
    current_letter = int(callback.data.replace('prev_letter_', ''))
    all_letter_ids = await AsyncQuery.select_all_letter_ids()

    next_id = next_unordered_number(lst=all_letter_ids, current_number=current_letter, backward=True)
    next_letter = await AsyncQuery.select_letter(next_id)
    await AsyncQuery.update_user_current_letter(user_id=callback.from_user.id, new_letter_id=next_id)

    if next_letter:
        if next_letter.id == current_letter:
            return await callback.answer(text=LEXICON_letters["only_one_letter"])
        await callback.message.edit_text(
            text=next_letter.letter + f'\n\n{LEXICON_letters["added_by"]} {next_letter.user_name}',
            reply_markup=create_letter_keyboard(next_letter.id),
        )


@router.callback_query(F.data == "edit_letter")
async def process_edit_letter_button(callback: CallbackQuery, state: FSMContext):
    """Хендлер кнопки добавления письма"""
    await state.set_state(FSMStates.edit_letter)
    await callback.message.edit_text(text=LEXICON_letters["edit_letter"],
                                     reply_markup=create_return_menu_keyboard())


@router.message(StateFilter(FSMStates.edit_letter))
async def process_edit_letter(message: Message, state: FSMContext):
    try:
        current_letter = await AsyncQuery.select_user_current_letter(message.from_user.id)
        result = await AsyncQuery.update_letter(letter_id=current_letter,
                                                letter=message.text)
        print(result)
    except Exception as e:
        print(e)
        await message.answer(text=LEXICON_letters["edit_error"],
                             reply_markup=create_del_message_keyboard())
    else:
        await message.answer(text=LEXICON_letters["edit_success"],
                             reply_markup=create_del_message_keyboard())
    finally:
        await state.clear()