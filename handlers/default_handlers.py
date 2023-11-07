from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from database.queries import AsyncQuery
from lexicon.lexicon import LEXICON_default


router = Router()


@router.message(Command(commands=["start"]))
async def process_start_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=f"{LEXICON_default['greeting']} {message.from_user.first_name}!"
    )
    await message.answer(text=LEXICON_default["greeting-con"])
    if await AsyncQuery.select_user(message.from_user.id) is None:
        await AsyncQuery.insert_user(message.from_user.id, message.from_user.first_name)


@router.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_dictionary(message: Message):
    await message.answer(LEXICON_default["help"])


@router.message(Command(commands=["cancel"]), StateFilter(default_state))
async def process_cancel_message(message: Message):
    await message.answer(text=LEXICON_default["cancel-denied"] + ', ' + message.from_user.first_name + '.')


@router.message(Command(commands=["Cancel"]))
async def process_cancel_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=LEXICON_default["Cancel"])


@router.message(Command(commands=["my_info"]), StateFilter(default_state))
async def process_cancel_message(message: Message):
    user = await AsyncQuery.select_user(message.from_user.id)
    tpl = LEXICON_default["my_info"]
    await message.answer(
        text=f"{tpl[0]}\n"
        f"{tpl[1]} {user.answers}\n"
        f"{tpl[2]} {user.right_answers}\n"
        f"{tpl[3]} {user.wrong_answers}"
    )

@router.message(Command(commands=['urls']))
async def process_urls_command(message: Message):
    await message.answer(text=LEXICON_default['urls'])
