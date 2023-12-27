import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config.config import load_config
from handlers import (default_handlers, other_handlers, play_dict, read_book,
                      read_bookmarks, read_excerpt, read_letter, menu_handlers)
from keyboards.main_menu import set_main_menu
from middlewares.only_string_check import OnlyStringMessage
from middlewares.throttling import Throttling

from aiogram.fsm.storage.redis import RedisStorage
from os import name as os_name



async def main():
    # инициализация логирования и конфига бота
    logging.basicConfig(level=logging.DEBUG)
    config = load_config()

    # create_tables()  # функция создания таблиц ненужна пока используется alembic

    # инициализация кэширования
    storage = MemoryStorage()
    storage_throttling = RedisStorage.from_url('redis://localhost:6379/0')

    # инициализация бота и диспетчера
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    # установка кнопки меню
    await set_main_menu(bot)
    # очередь middleware
    dp.message.middleware(Throttling(storage=storage_throttling))
    dp.message.outer_middleware(OnlyStringMessage())

    # очередь хендлеров
    dp.include_router(menu_handlers.router)
    dp.include_router(default_handlers.router)
    dp.include_router(read_book.router)
    dp.include_router(read_excerpt.router)
    dp.include_router(read_letter.router)
    dp.include_router(read_bookmarks.router)
    dp.include_router(play_dict.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()) # =['message', 'callback_query'] или =[]


if __name__ == "__main__":
    try:
        if os_name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")
