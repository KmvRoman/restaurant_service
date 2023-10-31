from aiogram import types, Bot
from aiogram.fsm.context import FSMContext

from src.application.get_address_from_location.dto import GetAddressFromLocationDtoInput
from src.application.read_nearest_location_id.dto import ReadNearestLocationDtoInput
from src.application.read_user_addresses.dto import GetUserAddressesDtoInput
from src.application.read_user_location_by_address.dto import ReadUserLocationByAddressDtoInput
from src.domain.order.constants.order import OrderType
from src.domain.order.entities.order import Location
from src.domain.restaurant.entities.restaurant_view import RestaurantId
from src.domain.user.entities.user import User
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.presentation.bot.content.fasade.interfaces import IContent
from src.presentation.bot.states.state_data.order import ShippingData
from src.presentation.bot.states.user.order import OrderStateShipping


async def selected_shipping(
        message: types.Message, bot: Bot, content: IContent, ioc: InteractorFactory,
        state: FSMContext, user: User,
):
    await message.delete()
    data = await state.get_data()
    if data.get("shipping_order") is None:
        await state.update_data(shipping_order=ShippingData(user_id=user.id).model_dump())
    user_addresses_case = await ioc.read_user_addresses()
    addresses = await user_addresses_case(data=GetUserAddressesDtoInput(user_id=user.id))
    await bot.send_message(
        chat_id=message.from_user.id, text=content.text.send_location_in_shipping(),
        reply_markup=content.reply.send_location_shipping(payload=addresses)
    )


async def get_user_location(
        message: types.Message, bot: Bot, content: IContent, ioc: InteractorFactory,
        state: FSMContext, restaurant: RestaurantId, user: User,
):
    read_nearest_restaurant_location_case = await ioc.read_nearest_restaurant_location_id()
    nearest_restaurant_location = await read_nearest_restaurant_location_case(data=ReadNearestLocationDtoInput(
        restaurant_id=restaurant, user_location=Location(
            longitude=message.location.longitude, latitude=message.location.latitude,
        )
    ))
    read_address_case = await ioc.get_address_from_location()
    address = await read_address_case(data=GetAddressFromLocationDtoInput(location=Location(
        longitude=message.location.longitude, latitude=message.location.latitude,
    )))
    data = await state.get_data()
    order = ShippingData(**data.get("shipping_order"))
    order.address = address.address
    order.location = Location(longitude=message.location.longitude, latitude=message.location.latitude)
    await state.update_data(shipping_order=order.model_dump())
    await bot.send_message(
        chat_id=message.from_user.id,
        text=content.text.show_webapp_button_in_shipping(order.address),
        reply_markup=content.reply.webapp_input_keyboard(
            user_id=user.id, restaurant_id=restaurant, user_location=Location(
                longitude=message.location.longitude, latitude=message.location.latitude,
            ), language=user.language,
            restaurant_location_id=nearest_restaurant_location.restaurant_location_id,
            order_type=OrderType.shipping,
        ),
    )


async def get_user_address(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
        ioc: InteractorFactory, restaurant: RestaurantId, user: User,
):
    read_location_case = await ioc.read_user_location_by_address()
    location = await read_location_case(data=ReadUserLocationByAddressDtoInput(address=message.text, user_id=user.id))
    read_nearest_restaurant_location_case = await ioc.read_nearest_restaurant_location_id()
    nearest_restaurant_location = await read_nearest_restaurant_location_case(data=ReadNearestLocationDtoInput(
        restaurant_id=restaurant, user_location=Location(
            longitude=location.location.longitude, latitude=location.location.latitude,
        )
    ))
    data = await state.get_data()
    order = ShippingData(**data.get("shipping_order"))
    order.address = message.text
    order.location = location.location
    await state.update_data(shipping_order=order.model_dump())
    await bot.send_message(
        chat_id=message.from_user.id,
        text=content.text.show_webapp_button_in_shipping(order.address),
        reply_markup=content.reply.webapp_input_keyboard(
            user_id=user.id, restaurant_id=restaurant, user_location=Location(
                longitude=message.location.longitude, latitude=message.location.latitude,
            ), language=user.language,
            restaurant_location_id=nearest_restaurant_location.restaurant_location_id,
            order_type=OrderType.shipping,
        ),
    )
