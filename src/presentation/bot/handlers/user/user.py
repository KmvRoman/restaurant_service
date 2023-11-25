from aiogram import Bot, Router, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

from src.application.edit_user_language.dto import UpdateUserLanguageDtoInput
from src.application.edit_user_name.dto import EditUserNameDtoInput
from src.application.edit_user_phone.dto import UpdateUserPhoneDtoInput
from src.application.read_restaurant_data.dto import ReadRestaurantDataDtoInput
from src.application.read_restaurant_location.dto import ReadLocationDtoInput
from src.application.read_restaurants.dto import ReadRestaurantsDtoInput
from src.domain.restaurant.entities.restaurant_view import RestaurantId, LocationId
from src.domain.user.constants.user import Language
from src.domain.user.entities.user import User
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.presentation.bot.content.fasade.interfaces import IContent
from src.presentation.bot.content.text_content.keyboard_content.reply.enums import MainMenu, Back
from src.presentation.bot.states.common.start import StartStates
from src.presentation.bot.states.user.order import OrderStatePickUp, OrderStateShipping

profile_router = Router(name="Profile Router")


@profile_router.message(CommandStart())
@profile_router.message(F.text.in_([i.back for i in Back.__subclasses__()]), StateFilter(StartStates))
async def command_start(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
):
    await bot.send_message(
        chat_id=message.from_user.id, text=content.text.greeting(),
        reply_markup=content.reply.users_main_menu(),
    )
    await state.clear()
    await state.set_state(StartStates.start)


@profile_router.message(
    StateFilter(OrderStatePickUp.pickup, OrderStateShipping.shipping),
    F.text.in_([i.back for i in Back.__subclasses__()]),
)
@profile_router.message(
    F.text.in_([i.menu for i in MainMenu.__subclasses__()]),
    StateFilter(StartStates),
)
async def choose_order_type(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
):
    await message.delete()
    await bot.send_message(
        chat_id=message.from_user.id, text=content.text.choose_order_method(),
        reply_markup=content.reply.choose_order_type_keyboard(),
    )
    await state.set_state(StartStates.start_order)


@profile_router.message(
    F.text.in_([i.info for i in MainMenu.__subclasses__()]),
    StateFilter(StartStates, None),
)
async def get_restaurant_info(
        message: types.Message, bot: Bot,
        ioc: InteractorFactory, user: User,
        content: IContent, state: FSMContext, restaurant: RestaurantId,
):
    restaurant_data = await ioc.read_restaurant_data()
    restaurant_info = await restaurant_data(
        data=ReadRestaurantDataDtoInput(
            restaurant_id=RestaurantId(restaurant),
            language=user.language,
        )
    )
    restaurant_addresses = await ioc.read_restaurants()
    locations = await restaurant_addresses(data=ReadRestaurantsDtoInput(restaurant_id=restaurant))
    await bot.send_message(
        chat_id=message.from_user.id,
        text=content.text.restaurant_info(name=restaurant_info.name, description=restaurant_info.description),
        reply_markup=await content.inline.restaurant_info_keyboard(restaurant_addresses=locations)
    )
    await state.set_state(StartStates.restaurant_location)


@profile_router.callback_query(StartStates.restaurant_location)
async def answer_concrete_restaurant_location(
        call: types.CallbackQuery, bot: Bot,
        ioc: InteractorFactory, content: IContent,
):
    data = await ioc.read_restaurant_location()
    restaurant_location = await data(data=ReadLocationDtoInput(location_id=LocationId(int(call.data))))
    message = await bot.send_message(
        chat_id=call.from_user.id,
        text=content.text.location_address(address=restaurant_location.address),
    )
    await bot.send_location(
        chat_id=call.from_user.id,
        longitude=restaurant_location.location.longitude,
        latitude=restaurant_location.location.latitude,
        reply_to_message_id=message.message_id,
    )
    await call.answer()


@profile_router.callback_query(F.data == "back", StateFilter(StartStates))
@profile_router.message(
    F.text.in_([i.settings for i in MainMenu.__subclasses__()]),
    StateFilter(StartStates, None),
)
async def open_settings(
        message: types.Message, bot: Bot,
        content: IContent, user: User, state: FSMContext,
):
    if isinstance(message, types.CallbackQuery):
        await bot.edit_message_text(
            chat_id=message.from_user.id, message_id=message.message.message_id,
            text=content.text.profile_settings_text(name=user.name, phone=user.phone, language=user.language),
            reply_markup=content.inline.user_settings_keyboard(),
        )
        await message.answer()
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=content.text.profile_settings_text(name=user.name, phone=user.phone, language=user.language),
            reply_markup=content.inline.user_settings_keyboard(),
        )
    await state.set_state(StartStates.settings)


@profile_router.callback_query(StartStates.settings, F.data == "change_name")
async def prepare_change_name(
        call: types.CallbackQuery, bot: Bot,
        content: IContent, state: FSMContext,
):
    await bot.edit_message_text(
        chat_id=call.from_user.id, message_id=call.message.message_id,
        text=content.text.input_name(), reply_markup=content.inline.back_button(),
    )
    await state.set_state(StartStates.change_name)
    await call.answer()


@profile_router.message(StartStates.change_name)
async def change_name(
        message: types.Message, bot: Bot, user: User,
        ioc: InteractorFactory, content: IContent, state: FSMContext,
):
    change_name_case = await ioc.edit_user_name()
    await change_name_case(data=EditUserNameDtoInput(user=user, name=message.text))
    await bot.send_message(
        chat_id=message.from_user.id,
        text=content.text.profile_settings_text(name=user.name, phone=user.phone, language=user.language),
        reply_markup=content.inline.user_settings_keyboard(),
    )
    await state.set_state(StartStates.settings)


@profile_router.callback_query(StartStates.settings, F.data == "change_phone")
async def prepare_change_phone(
        call: types.CallbackQuery, bot: Bot,
        content: IContent, state: FSMContext,
):
    await bot.edit_message_text(
        chat_id=call.from_user.id, message_id=call.message.message_id,
        text=content.text.input_phone(), reply_markup=content.inline.back_button(),
    )
    await state.set_state(StartStates.change_phone)
    await call.answer()


@profile_router.message(StartStates.change_phone)
async def change_phone(
        message: types.Message, bot: Bot, user: User,
        ioc: InteractorFactory, content: IContent, state: FSMContext,
):
    change_phone_case = await ioc.edit_user_phone()
    await change_phone_case(data=UpdateUserPhoneDtoInput(user=user, phone=message.text))
    await bot.send_message(
        chat_id=message.from_user.id,
        text=content.text.profile_settings_text(name=user.name, phone=user.phone, language=user.language),
        reply_markup=content.inline.user_settings_keyboard(),
    )
    await state.set_state(StartStates.settings)


@profile_router.callback_query(StartStates.settings, F.data == "change_language")
async def prepare_change_language(
        call: types.CallbackQuery, bot: Bot,
        content: IContent, state: FSMContext,
):
    await bot.edit_message_text(
        chat_id=call.from_user.id, message_id=call.message.message_id,
        text=content.text.input_language(), reply_markup=content.inline.change_language_keyboard(),
    )
    await state.set_state(StartStates.change_language)
    await call.answer()


@profile_router.callback_query(StartStates.change_language)
async def change_language(
        call: types.CallbackQuery, bot: Bot, user: User,
        ioc: InteractorFactory, content: IContent, state: FSMContext,
):
    change_language_case = await ioc.edit_user_language()
    await change_language_case(data=UpdateUserLanguageDtoInput(user=user, language=Language(call.data)))
    await bot.edit_message_text(
        chat_id=call.from_user.id, message_id=call.message.message_id,
        text=content.text.profile_settings_text(name=user.name, phone=user.phone, language=user.language),
        reply_markup=content.inline.user_settings_keyboard(),
    )
    await state.set_state(StartStates.settings)
    await call.answer()
