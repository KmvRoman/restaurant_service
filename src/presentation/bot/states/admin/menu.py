from aiogram.fsm.state import StatesGroup, State


class AdminMenuState(StatesGroup):
    choose_branch = State()
    choose_menu = State()
    product_menu = State()
    stop_list = State()
    categories = State()
    category_products = State()
    product = State()
    edit_product = State()
    edit_photo = State()
    edit_name = State()
    edit_description = State()
    edit_default_price = State()
    edit_extend_price = State()
    edit_price_name = State()
    delete_product_process = State()


class StopListState(StatesGroup):
    product = State()
    edit_product = State()
    edit_photo = State()
    edit_name = State()
    edit_description = State()
    edit_default_price = State()
    edit_extend_price = State()
    edit_price_name = State()
    delete_product_process = State()
