from aiogram.fsm.state import StatesGroup, State


class UserProfileState(StatesGroup):
    settings = State()
    change_name = State()
    change_phone = State()
    change_language = State()
