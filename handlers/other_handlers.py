from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon import LEXICON_default


router = Router()


@router.message()
async def send_echo(message: Message):
    try:
        await message.answer(text=LEXICON_default["unknown"])
    except TypeError:
        await message.reply(text=LEXICON_default["unknown"])
