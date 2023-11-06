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
from states.bot_states import FSMStates
from tts.tts import text_to_speech

router = Router()


@router.callback_query(F.data == "close_excerpts")
async def process_close_excerpts(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete_reply_markup()
    await callback.message.delete()


@router.callback_query(F.data == "close_top_excerpts")
async def process_close_excerpts(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete_reply_markup()
    await callback.message.delete()


@router.message(
    Command(commands=["cancel", "отмена"]), StateFilter(FSMStates.reading_excerpts)
)
async def process_cancel_excerpt(message: Message, state: FSMContext):
    await message.answer(text="Отмена области команд работы с отрывками")
    await state.clear()


@router.message(
    Command(commands=["cancel", "отмена"]), StateFilter(FSMStates.adding_excerpt)
)
async def process_cancel_adding_excerpt(message: Message, state: FSMContext):
    await message.answer(text="Ввод отменен")
    await state.clear()


@router.callback_query(F.data.startswith('skip_excerpt_'))
async def process_next_excerpt_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.reading_excerpts)
    previous_excerpt = callback.data.replace('skip_excerpt_', '')
    tpl_text = await AsyncQuery.select_random_excerpt(int(previous_excerpt))
    if tpl_text:
        await callback.message.edit_text(
            text=tpl_text[0] + f"\n\n...добавил: {tpl_text[2]}",
            reply_markup=create_rating_keyboard(tpl_text[1]),
        )


@router.message(
    Command(commands=["random_excerpt", "отрывок"]), StateFilter(default_state)
)
async def process_random_excerpt(message: Message, state: FSMContext):
    await state.set_state(FSMStates.reading_excerpts)
    # запрос кортежа (текст, порядковый номер, имя добавившего)
    tpl_text = await AsyncQuery.select_random_excerpt()
    if tpl_text:
        await message.answer(
            text=tpl_text[0] + f"\n\n...добавил: {tpl_text[2]}",
            reply_markup=create_rating_keyboard(tpl_text[1]),
        )
    else:
        await message.answer(
            text="Список отрывков пуст. Добавьте отрывок командой /offer_excerpt"
        )


@router.message(Command(commands=["read_top_excerpts"]))
async def process_read_excerpts(message: Message, state: FSMContext):
    await state.set_state(FSMStates.reading_excerpts)
    await AsyncQuery.load_top_excerpts()
    await message.answer(
        text=usertextcache[0], reply_markup=create_topexcerpts_keyboard(0)
    )


@router.callback_query(IsRating(), StateFilter(FSMStates.reading_excerpts))
async def process_rating_button(callback: CallbackQuery):
    command = callback.data.split("_")
    if command[0] == "up":
        await AsyncQuery.update_excerpt_rating(int(command[1]), "up")
    elif command[0] == "down":
        await AsyncQuery.update_excerpt_rating(int(command[1]), "down")
    tpl_text = await AsyncQuery.select_random_excerpt(int(command[1]))
    if tpl_text:
        await callback.message.edit_text(
            text=tpl_text[0] + f"\n\n...добавил: {tpl_text[2]}",
            reply_markup=create_rating_keyboard(tpl_text[1]),
        )


@router.callback_query(IsTTSExcerpts(), StateFilter(FSMStates.reading_excerpts))
async def process_voice_excerpts(callback: CallbackQuery, bot: Bot):
    text = await AsyncQuery.select_excerpt(
        int(callback.data.replace("voice-excerpt-", ""))
    )
    text_to_speech(text, callback.from_user.id)
    audio = FSInputFile(
        path=f"tts/{callback.from_user.id}-tts.mp3", filename=f"{text[:13]}.mp3"
    )
    async with ChatActionSender.upload_document(chat_id=callback.message.chat.id):
        await bot.send_audio(callback.message.chat.id, audio=audio)


@router.callback_query(IsTTSTopExcerpts(), StateFilter(FSMStates.reading_excerpts))
async def process_voice_top_excerpts(callback: CallbackQuery, bot: Bot):
    text = usertextcache[int(callback.data.replace("voice-top-excerpt-", ""))]
    text_to_speech(text, callback.from_user.id)
    audio = FSInputFile(
        path=f"tts/{callback.from_user.id}-tts.mp3", filename=f"{text[:13]}.mp3"
    )
    async with ChatActionSender.upload_document(chat_id=callback.message.chat.id):
        await bot.send_audio(callback.message.chat.id, audio=audio)


@router.message(
    Command(commands=["предложить_отрывок", "add_excerpt"]), StateFilter(default_state)
)
async def process_offer_excerpt(message: Message, state: FSMContext):
    await state.set_state(FSMStates.adding_excerpt)
    await message.answer(
        text="Введите целиком отрывок, которым хотите поделиться.\n"
        "/cancel - отмена ввода"
    )


@router.callback_query(IsNextTopExcerpt(), StateFilter(FSMStates.reading_excerpts))
async def process_next_top_excerpt_button(callback: CallbackQuery, state: FSMContext):
    if await state.get_state() == FSMStates.reading_excerpts:
        pass
    else:
        await state.set_state(FSMStates.reading_excerpts)
    next_pos = (int(callback.data.replace("next_", "")) + 1) % 3
    await AsyncQuery.load_top_excerpts()
    await callback.message.edit_text(
        text=usertextcache[next_pos], reply_markup=create_topexcerpts_keyboard(next_pos)
    )
    await callback.answer()


@router.message(StateFilter(FSMStates.adding_excerpt))
async def process_add_excerpt(message: Message, state: FSMContext):
    try:
        await AsyncQuery.insert_user_excerpt(message.text, message.from_user.first_name)
    except Exception as e:
        print(e)
        await message.answer(text="Ошибка при добавлении отрывка")
    else:
        await message.answer(text="Отрывок добавлен")
    finally:
        await state.clear()


@router.callback_query(F.data.startswith("report_excerpt_"))
async def process_report_excerpt_button(callback: CallbackQuery):
    await AsyncQuery.insert_questionable_excerpt(callback.data)
    await callback.answer("Отрывок отправлен на проверку")
