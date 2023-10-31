from aiogram import Router, types, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.domain.user.entities.user import User
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.infrastructure.web.s3.client import S3Client
from src.presentation.bot.content.fasade.interfaces import IContent
from src.presentation.bot.handlers.common.product import (
    product_card, admin_edit_product_menu, prepare_upload_photo_admin, upload_photo_admin,
    prepare_upload_name_admin, upload_name_admin, prepare_upload_description_admin,
    upload_description_admin, prepare_upload_default_price_admin, upload_default_price_admin,
    prepare_upload_extend_price_admin, upload_extend_price_admin, upload_price_name_admin,
    remove_price_admin, accept_update_price_admin, change_menu_product_status_admin,
    remove_product_stop_list_admin, accept_delete_product_admin_from_stop_list,
    show_stop_list_by_restaurant_location_admin,
)
from src.presentation.bot.states.admin.menu import AdminMenuState, StopListState

stop_router = Router()


@stop_router.callback_query(F.data == "back", StopListState.product)
@stop_router.callback_query(F.data == "stop_list", AdminMenuState.choose_menu)
async def show_stop_list_by_restaurant_location(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
        ioc: InteractorFactory, user: User,
):
    await show_stop_list_by_restaurant_location_admin(
        call=call, bot=bot, content=content, state=state, ioc=ioc, user=user,
    )
    await state.set_state(AdminMenuState.stop_list)


@stop_router.callback_query(
    F.data.in_(["back", "cancel_delete"]),
    StateFilter(StopListState.edit_product, StopListState.delete_product_process),
)
@stop_router.callback_query(AdminMenuState.stop_list)
async def show_stop_list_product(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
        ioc: InteractorFactory,
):
    await product_card(call=call, bot=bot, content=content, state=state, ioc=ioc)
    await state.set_state(StopListState.product)
    await call.answer()


@stop_router.callback_query(F.data == "remove_product", StopListState.product)
async def remove_product_stop_list(call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext):
    await remove_product_stop_list_admin(call=call, bot=bot, content=content)
    await state.set_state(StopListState.delete_product_process)
    await call.answer()


@stop_router.callback_query(F.data == "accept", StopListState.delete_product_process)
async def accept_delete_product(
        call: types.CallbackQuery, bot: Bot, content: IContent, ioc: InteractorFactory,
        state: FSMContext, user: User,
):
    await accept_delete_product_admin_from_stop_list(
        call=call, bot=bot, content=content, ioc=ioc, state=state, user=user,
    )
    await state.set_state(AdminMenuState.stop_list)


@stop_router.callback_query(F.data == "back", StateFilter(
    StopListState.edit_photo, StopListState.edit_name, StopListState.edit_description,
    StopListState.edit_default_price, StopListState.edit_extend_price,
))
@stop_router.callback_query(F.data == "edit_product", StopListState.product)
async def product_edit_menu(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory,
):
    await admin_edit_product_menu(call=call, bot=bot, content=content, state=state, ioc=ioc)
    await state.set_state(StopListState.edit_product)
    await call.answer()


@stop_router.callback_query(F.data == "change_photo", StopListState.edit_product)
async def prepare_upload_photo(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await prepare_upload_photo_admin(call=call, bot=bot, content=content)
    await state.set_state(StopListState.edit_photo)
    await call.answer()


@stop_router.message(F.photo, StopListState.edit_photo)
async def upload_photo(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
        ioc: InteractorFactory, s3: S3Client,
):
    await upload_photo_admin(message=message, bot=bot, content=content, state=state, ioc=ioc, s3=s3)
    await state.set_state(StopListState.product)


@stop_router.callback_query(F.data == "change_name", StopListState.edit_product)
async def prepare_upload_name(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await prepare_upload_name_admin(call=call, bot=bot, content=content, state=state)
    await state.set_state(StopListState.edit_name)
    await call.answer()


@stop_router.message(StopListState.edit_name)
async def upload_name(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory,
):
    await upload_name_admin(message=message, bot=bot, content=content, state=state, states=StopListState(), ioc=ioc)


@stop_router.callback_query(F.data == "change_description", StopListState.edit_product)
async def prepare_upload_description(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await prepare_upload_description_admin(call=call, bot=bot, content=content, state=state)
    await state.set_state(StopListState.edit_description)
    await call.answer()


@stop_router.message(StopListState.edit_description)
async def upload_description(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory,
):
    await upload_description_admin(
        message=message, bot=bot, content=content, state=state, states=StopListState(), ioc=ioc,
    )


@stop_router.callback_query(F.data == "change_default_price", StopListState.edit_product)
async def prepare_upload_default_price(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await prepare_upload_default_price_admin(call=call, bot=bot, content=content)
    await state.set_state(StopListState.edit_default_price)


@stop_router.message(StopListState.edit_default_price)
async def upload_default_price(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory,
):
    await upload_default_price_admin(message=message, bot=bot, content=content, state=state, ioc=ioc)
    await state.set_state(StopListState.product)


@stop_router.callback_query(F.data == "change_extend_price", StopListState.edit_product)
async def prepare_upload_extend_price(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await prepare_upload_extend_price_admin(call=call, bot=bot, content=content)
    await state.set_state(StopListState.edit_extend_price)


@stop_router.message(StopListState.edit_extend_price)
async def upload_extend_price(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
):
    await upload_extend_price_admin(message=message, bot=bot, content=content, state=state)
    await state.set_state(StopListState.edit_price_name)


@stop_router.message(StopListState.edit_price_name)
async def upload_price_name(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory,
):
    await upload_price_name_admin(
        message=message, bot=bot, content=content,
        state=state, ioc=ioc, states=StopListState(),
    )


@stop_router.callback_query(F.data.startswith("remove_price"), StopListState.edit_product)
async def remove_price(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory
):
    await remove_price_admin(call=call, bot=bot, content=content, state=state, ioc=ioc)
    await call.answer()


@stop_router.callback_query(F.data == "accept", StopListState.edit_product)
async def accept_update_price(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory,
):
    await accept_update_price_admin(call=call, bot=bot, content=content, state=state, ioc=ioc)
    await state.set_state(StopListState.product)


@stop_router.callback_query(F.data.in_(["not_available", "available"]), StopListState.product)
async def change_menu_product_status(
        call: types.CallbackQuery, bot: Bot, content: IContent,
        state: FSMContext, ioc: InteractorFactory,
):
    status = await change_menu_product_status_admin(call=call, bot=bot, content=content, state=state, ioc=ioc)
    await state.set_state(StopListState.product)
    await call.answer(text=content.text.change_menu_product_status_call_answer(status=status), show_alert=True)
