from aiogram.fsm.state import StatesGroup, State


class OrderStatePickUp(StatesGroup):
    pickup = State()
    send_location = State()
    phone = State()
    accept_order = State()
    charge_type = State()
    charge_url = State()


class OrderStateShipping(StatesGroup):
    shipping = State()
    send_location = State()
    comment = State()
    phone = State()
    accept_order = State()
    charge_type = State()
    charge_url = State()
