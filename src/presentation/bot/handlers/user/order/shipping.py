from aiogram import Router, F, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.application.common.exceptions import UserLocationNotFound
from src.domain.restaurant.entities.restaurant_view import RestaurantId
from src.domain.user.entities.user import User
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.presentation.bot.content.fasade.interfaces import IContent
from src.presentation.bot.content.text_content.keyboard_content.reply.enums import ChooseOrderType, Back
from src.presentation.bot.handlers.user.order.order_process.shipping import (
    selected_shipping, get_user_location, get_user_address,
)
from src.presentation.bot.states.common.start import StartStates
from src.presentation.bot.states.user.order import OrderStateShipping

shipping = Router()


@shipping.message(F.text.in_([i.back for i in Back.__subclasses__()]), OrderStateShipping.send_location)
@shipping.message(F.text.in_([i.shipping for i in ChooseOrderType.__subclasses__()]), StartStates.start_order)
async def choose_shipping(
        message: types.Message, bot: Bot, content: IContent, ioc: InteractorFactory,
        user: User, state: FSMContext,
):
    await selected_shipping(message=message, bot=bot, content=content, ioc=ioc, user=user, state=state)
    await state.set_state(OrderStateShipping.shipping)


@shipping.message(F.location, OrderStateShipping.shipping)
async def take_user_location(
        message: types.Message, bot: Bot, content: IContent, ioc: InteractorFactory, state: FSMContext,
        restaurant: RestaurantId, user: User,
):
    await get_user_location(
        message=message, bot=bot, content=content, ioc=ioc,
        state=state, restaurant=restaurant, user=user,
    )
    await state.set_state(OrderStateShipping.send_location)


@shipping.message(F.text.in_([i.back for i in Back.__subclasses__()]), OrderStateShipping.shipping)
@shipping.message(F.text, OrderStateShipping.shipping)
async def take_address(
        message: types.Message, bot: Bot, content: IContent, ioc: InteractorFactory, state: FSMContext,
        restaurant: RestaurantId, user: User,
):
    try:
        await get_user_address(
            message=message, bot=bot, content=content, state=state,
            ioc=ioc, restaurant=restaurant, user=user,
        )
        await state.set_state(OrderStateShipping.send_location)
    except UserLocationNotFound:
        return await bot.send_message(chat_id=message.from_user.id, text=content.text.user_address_not_found())


@shipping.message(
    F.text == "shipping",
    StateFilter(OrderStateShipping.send_location),
)  # TODO replace with real shipping handler
async def get_comment(message: types.Message, bot: Bot, content: IContent, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text=content.text.get_comment())


@shipping.message(OrderStateShipping.comment)
async def get_phone_number(message: types.Message, bot: Bot, content: IContent, state: FSMContext):
    pass


@shipping.message(OrderStateShipping.phone)
async def get_accept_order(message: types.Message, bot: Bot, content: IContent, state: FSMContext):
    pass


@shipping.message(OrderStateShipping.accept_order)
async def choose_type_charge(message: types.Message, bot: Bot, content: IContent, state: FSMContext):
    pass


@shipping.message(OrderStateShipping.charge_type)
async def send_url_for_charge(message: types.Message, bot: Bot, content: IContent, state: FSMContext):
    pass
