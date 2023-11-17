from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon import LEXICON_default
from keyboards.del_message_kb import create_del_message_keyboard


router = Router()


@router.message()
async def send_echo(message: Message):
    """'Отбойник'. Хендлер срабатывающий, если команда пользователя
    не обработана другими хендлерами. Присылает сообщение и возможных
    причинах игнорирования команды"""
    try:
        await message.answer(text=LEXICON_default["unknown"],
                             reply_markup=create_del_message_keyboard())
    except TypeError:
        await message.reply(text=LEXICON_default["unknown"],
                            reply_markup=create_del_message_keyboard())
