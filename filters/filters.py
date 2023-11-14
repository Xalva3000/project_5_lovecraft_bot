from re import fullmatch, match, search

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message


class IsPage(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        match_obj = fullmatch(r"/стр (\d{1,3})", message.text)
        if match_obj and int(match_obj.group(1)) in range(1, 252):
            return True
        return False


class IsCloseButton(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        buttons = ["close_excerpts", "close_top_excerpts", "cancel_bookmarks",
                   "close_top_excerpts", "close_book", "close_dct"]
        if callback.data in buttons:
            return True
        return False


class IsChapter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        match_obj = fullmatch(r"/фраг (\d{1,3})", message.text)
        if match_obj and int(match_obj.group(1)) in range(1, 151):
            return True
        return False


class IsRatio(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if search(r"\d+/\d{1,3}", callback.data):
            return True
        return False


class IsRating(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if fullmatch(r"up_\d+|down_\d+", callback.data):
            return True
        return False


class IsNextTopExcerpt(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if fullmatch(r"next_[012]", callback.data):
            return True
        return False


class IsTTSBook(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if match(r"voice-\d{1,3}", callback.data):
            return True
        return False


class IsTTSExcerpts(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if match(r"voice-excerpt-\d{1,3}", callback.data):
            return True
        return False


class IsTTSTopExcerpts(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if match(r"voice-top-excerpt-\d{1,3}", callback.data):
            return True
        return False


class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()


class IsDelBookmarkCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if fullmatch(r"\d{1,3}del", callback.data):
            return True
        return False


class IsAnswer(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if search(r"answer-", callback.data):
            return True
        return False


class IsDictPattern(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if search(r"\$\$", message.text):
            return True
        return False
