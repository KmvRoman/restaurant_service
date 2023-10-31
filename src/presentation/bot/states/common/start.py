from aiogram.fsm.state import State, StatesGroup


class StartStates(StatesGroup):
    start = State()
    restaurant_location = State()
    settings = State()
    change_name = State()
    change_phone = State()
    change_language = State()
    start_order = State()
