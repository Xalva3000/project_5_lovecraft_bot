from typing import Callable, Any, Dict, Awaitable
from aiogram.types import TelegramObject, Message
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import BaseMiddleware
from aiogram import Router
from lexicon.lexicon import LEXICON_default

router = Router()


class Throttling(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        user = f'user{event.from_user.id}'

        check_user = await self.storage.redis.get(name=user)

        if check_user:
            if int(check_user.decode()) >= 5:
                return await event.answer(text=LEXICON_default['spam'])
            elif int(check_user.decode()) < 5:
                await self.storage.redis.incr(name=user)
                return await handler(event, data)
        await self.storage.redis.set(name=user, value=1, ex=10)
        return await handler(event, data)
