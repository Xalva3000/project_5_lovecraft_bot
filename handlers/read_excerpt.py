from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.chat_action import ChatActionSender

from database.queries import AsyncQuery
from database.temporary_info import usertextcache
from filters.filters import (IsNextTopExcerpt, IsRating, IsTTSExcerpts,
                             IsTTSTopExcerpts)
from keyboards.rating_kb import create_rating_keyboard
from keyboards.topexcerpts_kb import create_topexcerpts_keyboard
from keyboards.return_menu_kb import create_return_menu_keyboard
from keyboards.del_message_kb import create_del_message_keyboard
from states.bot_states import FSMStates
from tts.tts import text_to_speech
from lexicon.lexicon import LEXICON_excerpts
from services.cashing import load_top_excerpts

router = Router()


@router.message(
    Command(commands=["cancel"]), StateFilter(FSMStates.reading_excerpts))
async def process_cancel_excerpt(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_excerpts["exit_excerpts"],
                         reply_markup=create_del_message_keyboard())
    await state.clear()


# @router.message(
#     Command(commands=["cancel"]), StateFilter(FSMStates.adding_excerpt)
# )
# async def process_cancel_adding_excerpt(message: Message, state: FSMContext):
#     await message.answer(text=LEXICON_excerpts["cancel_adding_excerpt"],
#                          reply_markup=create_return_menu_keyboard())
#     await state.clear()


@router.callback_query(F.data.startswith('skip_excerpt_'))
async def process_next_excerpt_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.reading_excerpts)
    previous_excerpt = callback.data.replace('skip_excerpt_', '')
    tpl_text = await AsyncQuery.select_random_excerpt(int(previous_excerpt))
    if tpl_text:
        await callback.message.edit_text(
            text=tpl_text[0] + f'\n\n{LEXICON_excerpts["added_by"]} {tpl_text[2]}',
            reply_markup=create_rating_keyboard(tpl_text[1]),
        )
    else:
        await callback.answer(text=LEXICON_excerpts["only_one_excerpt"])


@router.callback_query(IsRating(), StateFilter(FSMStates.reading_excerpts))
async def process_rating_button(callback: CallbackQuery):
    """Принимает команду на повышение или понижение (up_#) рейтинга
    определенного отрывка"""
    command = callback.data.split("_")
    await AsyncQuery.update_excerpt_rating(int(command[1]), command[0])

    tpl_text = await AsyncQuery.select_random_excerpt(int(command[1]))
    if tpl_text:
        await callback.message.edit_text(
            text=tpl_text[0] + f'\n\n{LEXICON_excerpts["added_by"]} {tpl_text[2]}',
            reply_markup=create_rating_keyboard(tpl_text[1]))
    else:
        await callback.answer(text=LEXICON_excerpts["mark_accepted"])


@router.callback_query(IsTTSExcerpts(), StateFilter(FSMStates.reading_excerpts))
async def process_voice_excerpts(callback: CallbackQuery, bot: Bot):
    text = await AsyncQuery.select_excerpt(
        int(callback.data.replace("voice-excerpt-", ""))
    )
    await text_to_speech(text, callback.from_user.id)
    audio = FSInputFile(
        path=f"tts/{callback.from_user.id}-tts.mp3", filename=f"{text[:13]}.mp3"
    )
    async with ChatActionSender.upload_document(chat_id=callback.message.chat.id):
        await bot.send_audio(callback.message.chat.id, audio=audio)


@router.callback_query(IsTTSTopExcerpts(), StateFilter(FSMStates.reading_excerpts))
async def process_voice_top_excerpts(callback: CallbackQuery, bot: Bot):
    text = usertextcache[int(callback.data.replace("voice-top-excerpt-", ""))]
    await text_to_speech(text, callback.from_user.id)
    audio = FSInputFile(
        path=f"tts/{callback.from_user.id}-tts.mp3", filename=f"{text[:13]}.mp3"
    )
    async with ChatActionSender.upload_document(chat_id=callback.message.chat.id):
        await bot.send_audio(callback.message.chat.id, audio=audio)


@router.callback_query(IsNextTopExcerpt(), StateFilter(FSMStates.reading_excerpts))
async def process_next_top_excerpt_button(callback: CallbackQuery, state: FSMContext):
    if await state.get_state() == FSMStates.reading_excerpts:
        pass
    else:
        await state.set_state(FSMStates.reading_excerpts)
    await load_top_excerpts()

    pos = int(callback.data.replace("next_", ""))
    if len(usertextcache) > 1:
        next_pos = (pos + 1) % len(usertextcache) if len(usertextcache) == 2 else (pos + 1) % 3
        await callback.message.edit_text(
            text=usertextcache[next_pos],
            reply_markup=create_topexcerpts_keyboard(next_pos)
        )
        await callback.answer()
    else:
        await callback.answer(text=LEXICON_excerpts["only_one_excerpt"])


@router.message(StateFilter(FSMStates.adding_excerpt))
async def process_add_excerpt(message: Message, state: FSMContext):
    try:
        await AsyncQuery.insert_user_excerpt(message.text, message.from_user.first_name)
    except Exception as e:
        print(e)
        await message.answer(text=LEXICON_excerpts["adding_error"])
    else:
        await message.answer(text=LEXICON_excerpts["adding_success"],
                             reply_markup=create_return_menu_keyboard())
    finally:
        await state.clear()


@router.callback_query(F.data.startswith("report_excerpt_"))
async def process_report_excerpt_button(callback: CallbackQuery):
    await AsyncQuery.insert_questionable_excerpt(callback.data)
    await callback.answer(text=LEXICON_excerpts["report_excerpt"])
