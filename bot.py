import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config.config import load_config
from database.database import create_tables
from handlers import (default_handlers, other_handlers, play_dict, read_book,
                      read_bookmarks, read_excerpt)
from keyboards.main_menu import set_main_menu

# from aiogram.fsm.storage.redis import Redis, RedisStorage


async def main():
    logging.basicConfig(level=logging.DEBUG)
    config = load_config()

    create_tables()
    storage = MemoryStorage()

    # redis = Redis()
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    # dp = Dispatcher(storage=RedisStorage(redis=redis))

    dp = Dispatcher(storage=storage)
    await set_main_menu(bot)

    dp.include_router(default_handlers.router)
    dp.include_router(read_book.router)
    dp.include_router(read_excerpt.router)
    dp.include_router(read_bookmarks.router)

    dp.include_router(play_dict.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")
