from aiogram.fsm.state import State, StatesGroup


class FSMStates(StatesGroup):
    reading_book = State()
    bookmarks_list = State()
    edit_bookmarks = State()
    reading_dict = State()
    reading_excerpts = State()
    adding_excerpt = State()
    edit_excerpt = State()
    adding_term = State()
    play_dict = State()
    reading_letters = State()
    adding_letter = State()
    edit_letter = State()
