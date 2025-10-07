from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.chat_action import ChatActionSender

from database.queries import AsyncQuery
from filters.filters import IsTTSExcerpts
from keyboards.excerpt_kb import create_excerpt_keyboard
from keyboards.return_menu_kb import create_return_menu_keyboard
from keyboards.del_message_kb import create_del_message_keyboard, create_del_audio_keyboard
from states.bot_states import FSMStates
from tts.tts import text_to_speech
from lexicon.lexicon import LEXICON_excerpts
from services.next_unordered_number import next_unordered_number

router = Router()


@router.message(
    Command(commands=["cancel"]), StateFilter(FSMStates.reading_excerpts))
async def process_cancel_excerpt(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_excerpts["exit_excerpts"],
                         reply_markup=create_del_message_keyboard())
    await state.clear()


@router.callback_query(IsTTSExcerpts(), StateFilter(FSMStates.reading_excerpts))
async def process_voice_excerpts(callback: CallbackQuery, bot: Bot):
    excerpt = await AsyncQuery.select_excerpt(
        int(callback.data.replace("voice-excerpt-", ""))
    )
    await text_to_speech(excerpt.excerpt, callback.from_user.id)
    audio = FSInputFile(
        path=f"tts/{callback.from_user.id}-tts.mp3", filename=f"{excerpt.excerpt[:13]}.mp3"
    )
    async with ChatActionSender.upload_document(bot=bot, chat_id=callback.message.chat.id):
        await bot.send_audio(callback.message.chat.id,
                             audio=audio,
                             reply_markup=create_del_audio_keyboard()
                             )


@router.message(StateFilter(FSMStates.adding_excerpt))
async def process_add_excerpt(message: Message, state: FSMContext):
    try:
        await AsyncQuery.insert_user_excerpt(message.text, message.from_user.first_name)
    except Exception as e:
        print(e)
        await message.answer(text=LEXICON_excerpts["adding_error"],
                             reply_markup=create_del_message_keyboard())
    else:
        await message.answer(text=LEXICON_excerpts["adding_success"],
                             reply_markup=create_del_message_keyboard())
    finally:
        await state.clear()


@router.callback_query(F.data.startswith('next_excerpt_'))
async def process_next_excerpt_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.reading_excerpts)
    current_excerpt = int(callback.data.replace('next_excerpt_', ''))
    all_excerpt_ids = await AsyncQuery.select_all_excerpt_ids()

    next_id = next_unordered_number(lst=all_excerpt_ids, current_number=current_excerpt)
    next_excerpt = await AsyncQuery.select_excerpt(next_id)
    await AsyncQuery.update_user_current_excerpt(callback.from_user.id, next_id)

    if next_excerpt:
        if next_excerpt.id == current_excerpt:
            return await callback.answer(text=LEXICON_excerpts["only_one_excerpt"])
        await callback.message.edit_text(
            text=next_excerpt.excerpt + f'\n\n{LEXICON_excerpts["added_by"]} {next_excerpt.user_name}',
            reply_markup=create_excerpt_keyboard(next_excerpt.id),
        )


@router.callback_query(F.data.startswith('prev_excerpt_'))
async def process_next_excerpt_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.reading_excerpts)
    current_excerpt = int(callback.data.replace('prev_excerpt_', ''))
    all_excerpt_ids = await AsyncQuery.select_all_excerpt_ids()

    next_id = next_unordered_number(lst=all_excerpt_ids, current_number=current_excerpt, backward=True)
    next_excerpt = await AsyncQuery.select_excerpt(next_id)
    await AsyncQuery.update_user_current_excerpt(callback.from_user.id, next_id)

    if next_excerpt:
        if next_excerpt.id == current_excerpt:
            return await callback.answer(text=LEXICON_excerpts["only_one_excerpt"])
        await callback.message.edit_text(
            text=next_excerpt.excerpt + f'\n\n{LEXICON_excerpts["added_by"]} {next_excerpt.user_name}',
            reply_markup=create_excerpt_keyboard(next_excerpt.id),
        )


# @router.callback_query(F.data.startswith("report_excerpt_"))
# async def process_report_excerpt_button(callback: CallbackQuery):
#     await AsyncQuery.insert_questionable_excerpt(callback.data)
#     await callback.answer(text=LEXICON_excerpts["report_excerpt"])


@router.callback_query(F.data.startswith("edit_excerpt_"))
async def process_edit_excerpt_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.edit_excerpt)
    await callback.message.edit_text(text=LEXICON_excerpts["edit_excerpt"],
                                     reply_markup=create_return_menu_keyboard())


@router.message(StateFilter(FSMStates.edit_excerpt))
async def process_edit_letter(message: Message, state: FSMContext):
    try:
        current_excerpt = await AsyncQuery.select_user_current_excerpt(message.from_user.id)
        await AsyncQuery.update_excerpt(excerpt_id=current_excerpt, excerpt=message.text)
    except Exception as e:
        print(e)
        await message.answer(text=LEXICON_excerpts["edit_error"],
                             reply_markup=create_del_message_keyboard())
    else:
        await message.answer(text=LEXICON_excerpts["edit_success"],
                             reply_markup=create_del_message_keyboard())
    finally:
        await state.clear()
