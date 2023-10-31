from aiogram.fsm.state import StatesGroup, State


class AddProductState(StatesGroup):
    menu = State()
    menu_upload_product = State()
    prepare_photo = State()
    add_photo = State()
    prepare_name = State()
    add_name = State()
    prepare_description = State()
    add_description = State()
    select_mode = State()
    add_default_price = State()
    add_extend_price = State()
    add_price_name = State()
