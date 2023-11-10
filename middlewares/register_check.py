from typing import Callable, Dict, Awaitable, Any, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from database.queries import AsyncQuery


class RegisterCheck(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        user = await AsyncQuery.select_user(event.from_user.id)
        if user is None:
            await AsyncQuery.insert_user(event.from_user.id)
        else:
            print(f'hello {user.name}')
            await event.answer(f'hello {user.name}')
        return await handler(event, data)
