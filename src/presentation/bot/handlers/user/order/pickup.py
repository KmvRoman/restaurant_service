from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram import Router, F, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.application.accept_order.dto import AcceptOrderDtoInput
from src.application.common.exceptions import RestaurantLocationIdNotFound, RestaurantLocationNotFound
from src.application.read_order_admin.dto import ReadAdminOrderDtoInput
from src.application.read_order_user.dto import ReadUserOrderDtoInput
from src.domain.order.constants.order import PaymentType
from src.domain.order.entities.order import OrderId
from src.domain.restaurant.entities.restaurant_view import RestaurantId
from src.domain.user.constants.user import Language
from src.domain.user.entities.user import User
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.presentation.bot.content.fasade.interfaces import IContent
from src.presentation.bot.content.initialize_content_factory import initialize_content
from src.presentation.bot.content.text_content.constants import ConcretePaymentTypeRu
from src.presentation.bot.content.text_content.keyboard_content.reply.enums import (
    ChooseOrderType, Back, Accept, PaymentTypes,
)
from src.presentation.bot.content.text_content.validation.phone_number_validation import validate_phone_number
from src.presentation.bot.handlers.common.order import create_order_pickup
from src.presentation.bot.handlers.user.order.order_process.pickup import (
    selected_pickup, get_restaurant_location, get_restaurant_location_by_user_location, exit_webapp_pick_up,
)
from src.presentation.bot.states.common.start import StartStates
from src.presentation.bot.states.state_data.order import PickupData
from src.presentation.bot.states.user.order import OrderStatePickUp

pickup = Router()


@pickup.message(
    F.text.in_([i.back for i in Back.__subclasses__()]),
    StateFilter(OrderStatePickUp.send_location, OrderStatePickUp.phone),
)
@pickup.message(F.text.in_([i.pickup for i in ChooseOrderType.__subclasses__()]), StartStates.start_order)
async def choose_pickup(
        message: types.Message, bot: Bot, content: IContent, ioc: InteractorFactory, restaurant: RestaurantId,
        state: FSMContext, user: User,
):
    await selected_pickup(
        message=message, bot=bot, content=content,
        ioc=ioc, restaurant=restaurant, state=state, user=user,
    )


@pickup.message(F.text, OrderStatePickUp.pickup)
async def get_restaurant_address(
        message: types.Message, bot: Bot, content: IContent, ioc: InteractorFactory,
        state: FSMContext, restaurant: RestaurantId, user: User,
):
    try:
        await get_restaurant_location(
            message=message, bot=bot, content=content,
            ioc=ioc, state=state, restaurant=restaurant, user=user,
        )
    except RestaurantLocationIdNotFound:
        return await bot.send_message(chat_id=message.from_user.id, text=content.text.restaurant_address_not_found())
    await state.set_state(OrderStatePickUp.send_location)


@pickup.message(F.location, OrderStatePickUp.pickup)
async def get_location(
        message: types.Message, bot: Bot, content: IContent, ioc: InteractorFactory, state: FSMContext,
        restaurant: RestaurantId, user: User,
):
    await get_restaurant_location_by_user_location(
        message=message, bot=bot, content=content, ioc=ioc,
        state=state, restaurant=restaurant, user=user,
    )
    await state.set_state(OrderStatePickUp.send_location)


@pickup.message(
    F.text.in_([i.back for i in Back.__subclasses__()]),
    StateFilter(OrderStatePickUp.accept_order, OrderStatePickUp.charge_type),
)
@pickup.message(F.web_app_data)
async def webapp_exit(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
        ioc: InteractorFactory, user: User,
):
    await message.delete()
    await exit_webapp_pick_up(message=message, bot=bot, content=content, state=state, ioc=ioc, user=user)
    await state.set_state(OrderStatePickUp.phone)


@pickup.message(F.text, OrderStatePickUp.phone)
async def get_phone_number_from_text(message: types.Message, bot: Bot, content: IContent, state: FSMContext):
    data = await state.get_data()
    order = PickupData(**data.get("pickup_order"))
    if not validate_phone_number(phone=message.text):
        await bot.send_message(chat_id=message.from_user.id, text=content.text.wrong_phone_number())
        return
    order.phone = message.text
    await state.update_data(pickup_order=order.model_dump())
    await bot.send_message(
        chat_id=message.from_user.id,
        text=content.text.accept_order_pickup(
            phone=order.phone, products=order.products, total_amount=order.total_amount),
    )
    await state.set_state(OrderStatePickUp.accept_order)


@pickup.message(F.contact, OrderStatePickUp.phone)
async def get_phone_number_from_button(message: types.Message, bot: Bot, content: IContent, state: FSMContext):
    data = await state.get_data()
    order = PickupData(**data.get("pickup_order"))
    order.phone = message.contact.phone_number
    await state.update_data(pickup_order=order.model_dump())
    await bot.send_message(
        chat_id=message.from_user.id,
        text=content.text.accept_order_pickup(
            phone=order.phone, products=order.products, total_amount=order.total_amount),
        reply_markup=content.reply.user_accept_order_keyboard(),
    )
    await state.set_state(OrderStatePickUp.accept_order)


@pickup.message(F.text.in_([i.back for i in Back.__subclasses__()]), OrderStatePickUp.charge_url)
@pickup.message(F.text.in_([i.accept for i in Accept.__subclasses__()]), OrderStatePickUp.accept_order)
async def accept_order(message: types.Message, bot: Bot, content: IContent, state: FSMContext):
    await bot.send_message(
        chat_id=message.from_user.id, text=content.text.choose_type_charge(),
        reply_markup=content.reply.payment_type_choose(),
    )
    await state.set_state(OrderStatePickUp.charge_type)


@pickup.message(F.text.in_([i.cache for i in PaymentTypes.__subclasses__()]), OrderStatePickUp.charge_type)
async def choose_cache(
        message: types.Message, bot: Bot, content: IContent,
        state: FSMContext, ioc: InteractorFactory, user: User,
):
    data = await state.get_data()
    admin_content = initialize_content()(language=Language.ru)
    order = PickupData(**data.get("pickup_order"))
    order.payment_type = PaymentType.cache
    try:
        order_id = await create_order_pickup(ioc=ioc, user=user, order=order)
    except RestaurantLocationNotFound:
        await bot.send_message(chat_id=message.from_user.id, text=content.text.restaurant_address_not_found())
        return
    order.order_id = order_id
    await state.update_data(pickup_order=order.model_dump())
    get_group_id = await ioc.read_branch_group()
    group_id = await get_group_id(restaurant_location_id=order.restaurant_location_id)

    get_order_for_admin = await ioc.read_order_admin()
    admin_order = await get_order_for_admin(data=ReadAdminOrderDtoInput(order_id=order_id, language=Language.ru))
    await bot.send_message(
        chat_id=group_id,
        text=admin_content.text.send_order_to_admins_pickup(
            order_id=admin_order.order_id, first_name=admin_order.name,
            payment_type=ConcretePaymentTypeRu.cache, phone=admin_order.phone, total_amount=admin_order.total_cost,
            products=admin_order.products,
        ),
        reply_markup=admin_content.inline.accept_order_admin_keyboard_pickup(order_id=order_id),
    )

    get_order_user = await ioc.read_order_user()
    user_order = await get_order_user(data=ReadUserOrderDtoInput(order_id=order_id, language=user.language))

    await bot.send_message(chat_id=message.from_user.id, text=content.text.send_finish_order_presentation_pickup(
        order_id=order_id, products=user_order.products, total_amount=user_order.total_cost,
    ), reply_markup=content.reply.users_main_menu())
    await state.set_state(StartStates.start)


@pickup.message(F.text.in_([i.payme for i in PaymentTypes.__subclasses__()]), OrderStatePickUp.charge_type)
async def choose_payme(
        message: types.Message, bot: Bot, content: IContent,
        state: FSMContext, ioc: InteractorFactory, user: User,
):
    data = await state.get_data()
    order = PickupData(**data.get("pickup_order"))
    order_id = await create_order_pickup(ioc=ioc, user=user, order=order)
    order.order_id = order_id
    await state.update_data(pickup_order=order.model_dump())
    await state.set_state(OrderStatePickUp.charge_url)


@pickup.message(F.text.in_([i.click for i in PaymentTypes.__subclasses__()]), OrderStatePickUp.charge_type)
async def choose_click(
        message: types.Message, bot: Bot, content: IContent,
        state: FSMContext, ioc: InteractorFactory, user: User,
):
    data = await state.get_data()
    order = PickupData(**data.get("pickup_order"))
    order_id = await create_order_pickup(ioc=ioc, user=user, order=order)
    order.order_id = order_id
    await state.update_data(pickup_order=order.model_dump())
    await state.set_state(OrderStatePickUp.charge_url)


@pickup.callback_query(F.data.startswith("adp_"))
async def accept_pickup_order_from_admin(
        call: types.CallbackQuery, bot: Bot, content: IContent,
        ioc: InteractorFactory, user_repo: UserRepository,
):
    order_id = OrderId(int(call.data.split("_")[1]))
    accept_order_case = await ioc.accept_order()
    acc_order = await accept_order_case(data=AcceptOrderDtoInput(order_id=order_id))
    telegram_id, language = await user_repo.telegram_id_from_user_id(user_id=acc_order.user_id)
    user_content = initialize_content()(language=language)
    with suppress(TelegramBadRequest):
        await bot.edit_message_reply_markup(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            reply_markup=content.inline.accepted_order_admin_keyboard_pickup(),
        )
    await bot.send_message(chat_id=telegram_id, text=user_content.text.accept_order_pickup_by_admin(order_id=order_id))
