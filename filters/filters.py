from re import fullmatch, match, search

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message


class IsPage(BaseFilter):
    """Фильтр сообщений вида /стр 1 (до фиксированного значения 251 для этого бота)."""
    async def __call__(self, message: Message) -> bool:
        match_obj = fullmatch(r"/стр (\d{1,3})", message.text)
        if match_obj and int(match_obj.group(1)) in range(1, 252):
            return True
        return False


class IsChapter(BaseFilter):
    """Фильтр сообщений вида /фраг 1 (до фиксированного значения 150 для этого бота)."""
    async def __call__(self, message: Message) -> bool:
        match_obj = fullmatch(r"/фраг (\d{1,3})", message.text)
        if match_obj and int(match_obj.group(1)) in range(1, 151):
            return True
        return False


class IsCloseButton(BaseFilter):
    """Фильтр сообщений от нажатия кнопок отмены и возврата в меню."""
    async def __call__(self, callback: CallbackQuery) -> bool:
        buttons = ["close_excerpts", "close_top_excerpts", "cancel_bookmarks",
                   "close_top_excerpts", "close_book", "close_dct", "return_menu"]
        if callback.data in buttons:
            return True
        return False


class IsDelMessageButton(BaseFilter):
    """Фильтр сообщений от нажатия кнопок удаления сообщения бота."""
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'del_message':
            return True
        return False


class IsRatio(BaseFilter):
    """Фильтр сообщений от нажатия кнопки отношения текущей страницы
    к общему кол-ву страниц в книге. (Кнопка для сохранения закладки)"""
    async def __call__(self, callback: CallbackQuery) -> bool:
        if search(r"\d+/\d{1,3}", callback.data):
            return True
        return False


class IsRating(BaseFilter):
    """Фильтр сообщений от нажатия кнопки при чтении случайного отрывка
    с изображением emoji 'большой палец поднят' или 'опущен', что означает
     повышение или понижения общей оценки отрывка."""
    async def __call__(self, callback: CallbackQuery) -> bool:
        if fullmatch(r"up_\d+|down_\d+", callback.data):
            return True
        return False


class IsNextTopExcerpt(BaseFilter):
    """Фильтр сообщений от нажатия кнопки '>>' при чтении лучших
    отрывков, с указанием индекса текущего отрывка. (0 - отрывок
    с наивысшей оценкой, 1 - второе место и тд)"""
    async def __call__(self, callback: CallbackQuery) -> bool:
        if fullmatch(r"next_[012]", callback.data):
            return True
        return False


class IsTTSBook(BaseFilter):
    """Фильтр сообщений от нажатия кнопки с изображением динамика,
    предназначенной для команды озвучивания текста фрагмента или главы книги.
    В сообщении также указан номер фрагмента."""
    async def __call__(self, callback: CallbackQuery) -> bool:
        if match(r"voice-\d{1,3}", callback.data):
            return True
        return False


class IsTTSExcerpts(BaseFilter):
    """Фильтр сообщений от нажатия кнопки с изображением динамика,
    предназначенной для команды озвучивания отрывка, выдержки.
    В сообщении также указан номер отрывка."""
    async def __call__(self, callback: CallbackQuery) -> bool:
        if match(r"voice-excerpt-\d{1,3}", callback.data):
            return True
        return False


class IsTTSTopExcerpts(BaseFilter):
    """Фильтр сообщений от нажатия кнопки с изображением динамика,
    предназначенной для команды озвучивания популярного отрывка, выдержки.
    В сообщении также указан индекс позиции отрывка."""

    async def __call__(self, callback: CallbackQuery) -> bool:
        if match(r"voice-top-excerpt-\d{1,3}", callback.data):
            return True
        return False


class IsDigitCallbackData(BaseFilter):
    """Фильтр сообщений от нажатия кнопки в которых содержатся исключительно цифры."""

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()


class IsDelBookmarkCallbackData(BaseFilter):
    """Фильтр сообщений от нажатия кнопки удаления закладки."""

    async def __call__(self, callback: CallbackQuery) -> bool:
        if fullmatch(r"\d{1,3}del", callback.data):
            return True
        return False


class IsAnswer(BaseFilter):
    """Фильтр сообщений от нажатия кнопки ответа в игре 'Словарь'."""

    async def __call__(self, callback: CallbackQuery) -> bool:
        if search(r"answer-", callback.data):
            return True
        return False


class IsDictPattern(BaseFilter):
    """Фильтр сообщений отправленных пользователем в состоянии ввода
    нового термина в игре 'Словарь'."""

    async def __call__(self, message: Message) -> bool:
        if search(r"\$\$", message.text):
            return True
        return False


