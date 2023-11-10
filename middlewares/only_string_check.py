from typing import Callable, Any, Dict, Awaitable
from aiogram import BaseMiddleware, Router
from aiogram.types import Message


router = Router()


class OnlyStringMessage(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event.text, str):
            return await handler(event, data)
        else:
            await event.send_copy(event.chat.id)
