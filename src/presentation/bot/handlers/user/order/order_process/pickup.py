from aiogram import types, Bot
from aiogram.fsm.context import FSMContext

from src.application.read_current_basket.dto import ReadCurrentBasketDtoInput
from src.application.read_nearest_location_id.dto import ReadNearestLocationDtoInput
from src.application.read_restaurant_addresses.dto import ReadRestaurantAddressesDtoInput
from src.application.read_restaurant_location_id_by_address.dto import ReadRestaurantLocationIdByAddressDtoInput
from src.domain.order.constants.order import OrderType
from src.domain.order.entities.order import Location
from src.domain.restaurant.entities.restaurant_view import RestaurantId
from src.domain.user.entities.user import User
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.presentation.bot.content.fasade.interfaces import IContent
from src.presentation.bot.states.state_data.order import PickupData
from src.presentation.bot.states.user.order import OrderStatePickUp


async def selected_pickup(
        message: types.Message, bot: Bot, content: IContent, ioc: InteractorFactory,
        state: FSMContext, restaurant: RestaurantId, user: User,
):
    await message.delete()
    data = await state.get_data()
    if data.get("pickup_order") is None:
        await state.update_data(pickup_order=PickupData(user_id=user.id).model_dump())
    restaurant_addresses_case = await ioc.read_restaurant_addresses()
    addresses = await restaurant_addresses_case(data=ReadRestaurantAddressesDtoInput(restaurant_id=restaurant))
    await bot.send_message(
        chat_id=message.from_user.id, text=content.text.send_location_in_pickup(),
        reply_markup=content.reply.send_location_pickup(payload=addresses)
    )
    await state.set_state(OrderStatePickUp.pickup)


async def get_restaurant_location(
        message: types.Message, bot: Bot, content: IContent, ioc: InteractorFactory, state: FSMContext,
        restaurant: RestaurantId, user: User,
):
    data = await state.get_data()
    get_restaurant_location_id_case = await ioc.read_restaurant_location_id_by_address()
    restaurant_location_id = await get_restaurant_location_id_case(
        data=ReadRestaurantLocationIdByAddressDtoInput(restaurant_id=restaurant, address=message.text),
    )
    order = PickupData(**data.get("pickup_order"))
    order.restaurant_location_id = restaurant_location_id.location_id
    await state.update_data(pickup_order=order.model_dump())
    await message.delete()
    await bot.send_message(
        chat_id=message.from_user.id,
        text=content.text.show_webapp_button_in_pick_up(address=message.text),
        reply_markup=content.reply.webapp_input_keyboard(
            user_id=user.id, restaurant_id=restaurant, user_location=None, language=user.language,
            restaurant_location_id=restaurant_location_id.location_id, order_type=OrderType.pickup,
        ),
    )


async def get_restaurant_location_by_user_location(
        message: types.Message, bot: Bot, content: IContent, ioc: InteractorFactory, state: FSMContext,
        restaurant: RestaurantId, user: User,
):
    read_nearest_restaurant_location_case = await ioc.read_nearest_restaurant_location_id()
    nearest_restaurant_location = await read_nearest_restaurant_location_case(data=ReadNearestLocationDtoInput(
        restaurant_id=restaurant, user_location=Location(
            longitude=message.location.longitude, latitude=message.location.latitude,
        )
    ))
    data = await state.get_data()
    order = PickupData(**data.get("pickup_order"))
    order.restaurant_location_id = nearest_restaurant_location.restaurant_location_id
    await state.update_data(pickup_order=order.model_dump())
    await bot.send_message(
        chat_id=message.from_user.id,
        text=content.text.show_webapp_button_in_pick_up(address=nearest_restaurant_location.address),
        reply_markup=content.reply.webapp_input_keyboard(
            user_id=user.id, restaurant_id=restaurant, user_location=Location(
                longitude=message.location.longitude, latitude=message.location.latitude,
            ), language=user.language,
            restaurant_location_id=nearest_restaurant_location.restaurant_location_id,
            order_type=OrderType.pickup,
        ),
    )


async def exit_webapp_pick_up(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
        ioc: InteractorFactory, user: User,
):
    data = await state.get_data()
    order = PickupData(**data.get("pickup_order"))
    current_basket_case = await ioc.read_current_basket()
    basket = await current_basket_case(data=ReadCurrentBasketDtoInput(
        user_id=user.id, user_location=None, restaurant_location_id=order.restaurant_location_id,
        order_type=OrderType.pickup, language=user.language,
    ))
    order.products = basket.prepared
    order.total_amount = basket.total_amount
    await state.update_data(pickup_order=order.model_dump())
    await bot.send_message(
        chat_id=message.from_user.id, text=content.text.get_phone(),
        reply_markup=content.reply.user_phone_number_keyboard(),
    )
