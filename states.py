from aiogram.dispatcher.filters.state import State, StatesGroup

class AdRequest(StatesGroup):
    waiting_for_name = State()
    waiting_for_link = State()
    waiting_for_comment = State()
