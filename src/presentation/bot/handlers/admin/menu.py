from aiogram import Router, Bot, types, F

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from src.application.read_branches.dto import ReadBranchesDtoInput
from src.application.read_categories.dto import ReadCategoriesDtoInput
from src.application.read_product_admin.dto import ReadProductDtoInput
from src.domain.restaurant.entities.restaurant_view import RestaurantId
from src.domain.user.entities.user import User
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.infrastructure.web.s3.client import S3Client
from src.presentation.bot.content.fasade.interfaces import IContent
from src.presentation.bot.content.text_content.keyboard_content.reply.enums import AdminHome, AdminMainMenu
from src.presentation.bot.handlers.common.product import (
    product_card, admin_edit_product_menu, prepare_upload_photo_admin, upload_photo_admin,
    prepare_upload_name_admin, upload_name_admin, prepare_upload_description_admin,
    upload_description_admin, prepare_upload_default_price_admin, upload_default_price_admin,
    prepare_upload_extend_price_admin, upload_extend_price_admin, upload_price_name_admin,
    remove_price_admin, accept_update_price_admin, change_menu_product_status_admin,
    remove_product_stop_list_admin, get_category_products_admin, accept_delete_product_admin_from_menu,
)
from src.presentation.bot.states.admin.menu import AdminMenuState
from src.presentation.bot.states.admin.product import AddProductState

admin = Router()


async def read_product(
        call: types.CallbackQuery | types.Message, bot: Bot, content: IContent, data: dict,
        ioc: InteractorFactory, state: FSMContext,
):
    read_product_case = await ioc.read_product_admin()
    product = await read_product_case(data=ReadProductDtoInput(menu_product_id=data.get("admin_menu_product_id")))
    await state.update_data(admin_product_id=product.id)
    if isinstance(call, types.CallbackQuery):
        await call.message.delete()
    if product.photo is None:
        await bot.send_message(
            chat_id=call.from_user.id, text=content.text.admin_product(
                name=product.name, description=product.description,
                mode=product.mode, price=product.price, menu_product_status=product.menu_product_status,
            ), reply_markup=content.inline.product_admin_keyboard(menu_product_status=product.menu_product_status),
        )
    else:
        await bot.send_photo(chat_id=call.from_user.id, photo=product.photo, caption=content.text.admin_product(
            name=product.name, description=product.description,
            mode=product.mode, price=product.price, menu_product_status=product.menu_product_status,
        ), reply_markup=content.inline.product_admin_keyboard(menu_product_status=product.menu_product_status))


@admin.message(
    StateFilter(AddProductState),
    F.text.in_([i.home for i in AdminHome.__subclasses__()]),
)
@admin.message(Command("admin"))
async def admin_menu(
        message: types.Message, bot: Bot,
        content: IContent, state: FSMContext,
):
    await bot.send_message(
        chat_id=message.from_user.id, text=content.text.greeting_administrator(),
        reply_markup=content.reply.administrators_main_menu())
    await state.clear()


@admin.callback_query(AdminMenuState.choose_menu, F.data == "back")
@admin.message(F.text.in_([i.menu for i in AdminMainMenu.__subclasses__()]))
async def choose_branch(
        message: types.Message | types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
        ioc: InteractorFactory, restaurant: RestaurantId,
):
    if isinstance(message, types.CallbackQuery):
        await message.message.delete()
        await message.answer()
    else:
        await message.delete()
    restaurant_branches_case = await ioc.read_branches()
    branches = await restaurant_branches_case(data=ReadBranchesDtoInput(restaurant_id=restaurant))
    await bot.send_message(
        chat_id=message.from_user.id, text=content.text.choose_branch(),
        reply_markup=content.inline.choose_branch(branches=branches),
    )
    await state.set_state(AdminMenuState.choose_branch)


@admin.callback_query(StateFilter(AdminMenuState.categories, AdminMenuState.stop_list), F.data == "back")
@admin.callback_query(AdminMenuState.choose_branch)
async def choose_menu(
        call: types.CallbackQuery, bot: Bot,
        content: IContent, state: FSMContext,
):
    data = await state.get_data()
    if call.data == "back":
        if data.get("admin_current_location_id") is None:
            return await bot.send_message(chat_id=call.from_user.id, text=content.text.location_id_not_found())
    else:
        await state.update_data(admin_current_location_id=int(call.data))
    await bot.edit_message_text(
        chat_id=call.from_user.id, message_id=call.message.message_id,
        text=content.text.choose_something(),
        reply_markup=content.inline.choose_menu_keyboard(),
    )
    await state.set_state(AdminMenuState.choose_menu)
    await call.answer()


@admin.callback_query(F.data == "back", AdminMenuState.category_products)
@admin.callback_query(F.data == "menu_admin", AdminMenuState.choose_menu)
async def category_products(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
        ioc: InteractorFactory, restaurant: RestaurantId, user: User,
):
    categories_case = await ioc.read_categories()
    categories = await categories_case(
        data=ReadCategoriesDtoInput(restaurant_id=restaurant, language=user.language)
    )
    await bot.edit_message_text(
        chat_id=call.from_user.id, message_id=call.message.message_id, text=content.text.categories(),
        reply_markup=content.inline.admin_menu_categories_keyboard(buttons=categories.categories),
    )
    await state.set_state(AdminMenuState.categories)
    await call.answer()


@admin.callback_query(F.data == "back", AdminMenuState.product)
@admin.callback_query(AdminMenuState.categories)
async def get_category_products(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
        ioc: InteractorFactory, user: User,
):
    await get_category_products_admin(call=call, bot=bot, content=content, state=state, ioc=ioc, user=user)
    await state.set_state(AdminMenuState.category_products)
    await call.answer()


@admin.callback_query(
    F.data.in_(["back", "cancel_delete"]),
    StateFilter(AdminMenuState.edit_product, AdminMenuState.delete_product_process),
)
@admin.callback_query(AdminMenuState.category_products)
async def get_product(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
        ioc: InteractorFactory,
):
    await product_card(call=call, bot=bot, content=content, state=state, ioc=ioc)
    await state.set_state(AdminMenuState.product)
    await call.answer()


@admin.callback_query(F.data == "remove_product", AdminMenuState.product)
async def remove_product_stop_list(call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext):
    await remove_product_stop_list_admin(call=call, bot=bot, content=content)
    await state.set_state(AdminMenuState.delete_product_process)
    await call.answer()


@admin.callback_query(F.data == "accept", AdminMenuState.delete_product_process)
async def accept_delete_product(
        call: types.CallbackQuery, bot: Bot, content: IContent, ioc: InteractorFactory,
        state: FSMContext, user: User,
):
    await accept_delete_product_admin_from_menu(
        call=call, bot=bot, content=content, ioc=ioc, state=state, user=user,
    )
    await state.set_state(AdminMenuState.category_products)
    await call.answer()


@admin.callback_query(F.data == "back", StateFilter(
    AdminMenuState.edit_photo, AdminMenuState.edit_name, AdminMenuState.edit_description,
    AdminMenuState.edit_default_price, AdminMenuState.edit_extend_price,
))
@admin.callback_query(F.data == "edit_product", AdminMenuState.product)
async def edit_product_menu(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory,
):
    await admin_edit_product_menu(call=call, bot=bot, content=content, state=state, ioc=ioc)
    await state.set_state(AdminMenuState.edit_product)
    await call.answer()


@admin.callback_query(F.data == "change_photo", AdminMenuState.edit_product)
async def prepare_upload_photo(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await prepare_upload_photo_admin(call=call, bot=bot, content=content)
    await state.set_state(AdminMenuState.edit_photo)
    await call.answer()


@admin.message(F.photo, AdminMenuState.edit_photo)
async def upload_photo(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
        ioc: InteractorFactory, s3: S3Client,
):
    await upload_photo_admin(message=message, bot=bot, content=content, state=state, ioc=ioc, s3=s3)
    await state.set_state(AdminMenuState.product)


@admin.callback_query(F.data == "change_name", AdminMenuState.edit_product)
async def prepare_upload_name(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await prepare_upload_name_admin(call=call, bot=bot, content=content, state=state)
    await state.set_state(AdminMenuState.edit_name)
    await call.answer()


@admin.message(AdminMenuState.edit_name)
async def upload_name(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory,
):
    await upload_name_admin(message=message, bot=bot, content=content, state=state, states=AdminMenuState(), ioc=ioc)


@admin.callback_query(F.data == "change_description", AdminMenuState.edit_product)
async def prepare_upload_description(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await prepare_upload_description_admin(call=call, bot=bot, content=content, state=state)
    await state.set_state(AdminMenuState.edit_description)
    await call.answer()


@admin.message(AdminMenuState.edit_description)
async def upload_description(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory,
):
    await upload_description_admin(
        message=message, bot=bot, content=content, state=state, states=AdminMenuState(), ioc=ioc,
    )


@admin.callback_query(F.data == "change_default_price", AdminMenuState.edit_product)
async def prepare_upload_default_price(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await prepare_upload_default_price_admin(call=call, bot=bot, content=content)
    await state.set_state(AdminMenuState.edit_default_price)


@admin.message(AdminMenuState.edit_default_price)
async def upload_default_price(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory,
):
    await upload_default_price_admin(message=message, bot=bot, content=content, state=state, ioc=ioc)
    await state.set_state(AdminMenuState.product)


@admin.callback_query(F.data == "change_extend_price", AdminMenuState.edit_product)
async def prepare_upload_extend_price(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await prepare_upload_extend_price_admin(call=call, bot=bot, content=content)
    await state.set_state(AdminMenuState.edit_extend_price)


@admin.message(AdminMenuState.edit_extend_price)
async def upload_extend_price(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
):
    await upload_extend_price_admin(message=message, bot=bot, content=content, state=state)
    await state.set_state(AdminMenuState.edit_price_name)


@admin.message(AdminMenuState.edit_price_name)
async def upload_price_name(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory,
):
    await upload_price_name_admin(
        message=message, bot=bot, content=content,
        state=state, ioc=ioc, states=AdminMenuState(),
    )


@admin.callback_query(F.data.startswith("remove_price"), AdminMenuState.edit_product)
async def remove_price(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory
):
    await remove_price_admin(call=call, bot=bot, content=content, state=state, ioc=ioc)
    await call.answer()


@admin.callback_query(F.data == "accept", AdminMenuState.edit_product)
async def accept_update_price(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory,
):
    await accept_update_price_admin(call=call, bot=bot, content=content, state=state, ioc=ioc)
    await state.set_state(AdminMenuState.product)


@admin.callback_query(F.data.in_(["not_available", "available"]), AdminMenuState.product)
async def change_menu_product_status(
        call: types.CallbackQuery, bot: Bot, content: IContent,
        state: FSMContext, ioc: InteractorFactory,
):
    status = await change_menu_product_status_admin(call=call, bot=bot, content=content, state=state, ioc=ioc)
    await state.set_state(AdminMenuState.product)
    await call.answer(text=content.text.change_menu_product_status_call_answer(status=status), show_alert=True)
