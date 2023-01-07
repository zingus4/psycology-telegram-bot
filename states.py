from aiogram.dispatcher.filters.state import State, StatesGroup


class BotStates(StatesGroup):
    start = State()
    smr = State()
    test = State()
    current_test = State()
    end_test = State()
