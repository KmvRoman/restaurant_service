from contextlib import suppress

from aiogram import types, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from src.application.common.exceptions import EmptyStopList, CategoryProductsIsEmpty
from src.application.delete_product_from_system.dto import DeleteProductDtoInput
from src.application.edit_product_available.dto import EditProductAvailableDtoInput
from src.application.edit_product_description.dto import EditProductDescriptionDtoInput
from src.application.edit_product_name.dto import EditProductNameDtoInput
from src.application.edit_product_photo.dto import EditProductPhotoDtoInput
from src.application.edit_product_price.dto import EditProductPriceDtoInput
from src.application.read_category_products.dto import ReadCategoryProductsDtoInput
from src.application.read_product_admin.dto import ReadProductDtoInput
from src.application.read_stop_list.dto import ReadStopListDtoInput
from src.domain.product.entities.product import ProductName, ProductDescription, ProductPrice, ProductPriceName
from src.domain.restaurant.constants.constants import MenuProductStatus
from src.domain.restaurant.entities.restaurant_view import CategoryId
from src.domain.user.entities.user import User
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.infrastructure.web.s3.client import S3Client
from src.presentation.bot.content.fasade.interfaces import IContent
from src.presentation.bot.handlers.admin.product.product import get_not_exist_language
from src.presentation.bot.handlers.admin.product.send_file import send_file
from src.presentation.bot.states.admin.menu import AdminMenuState, StopListState
from src.presentation.bot.states.state_data.product import (
    ProductPriceData, ProductNameData, ProductDescriptionData, ProductPriceNameData,
)


async def get_category_products_admin(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
        ioc: InteractorFactory, user: User,
):
    data = await state.get_data()
    if call.data in ("back", "accept"):
        if data.get("admin_category_id") is None:
            return await bot.send_message(chat_id=call.from_user.id, text=content.text.location_id_not_found())
    else:
        await state.update_data(admin_category_id=CategoryId(int(call.data)))
        data = await state.get_data()
    category_products_case = await ioc.read_category_products()
    try:
        products = await category_products_case(data=ReadCategoryProductsDtoInput(
            location_id=data.get("admin_current_location_id"), category_id=data.get("admin_category_id"),
            language=user.language,
        ))
    except CategoryProductsIsEmpty:
        return await bot.edit_message_text(
            chat_id=call.from_user.id, message_id=call.message.message_id,
            text=content.text.category_products_empty(), reply_markup=content.inline.back_button(),
        )
    await call.message.delete()
    await bot.send_message(
        chat_id=call.from_user.id, text=products.category_name,
        reply_markup=content.inline.category_products_keyboard(products=products.products),
    )


async def show_stop_list_by_restaurant_location_admin(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
        ioc: InteractorFactory, user: User,
):
    data = await state.get_data()
    stop_list_case = await ioc.read_stop_list()
    await call.message.delete()
    try:
        stop_list = await stop_list_case(ReadStopListDtoInput(
            location_id=data.get("admin_current_location_id"), language=user.language)
        )
    except EmptyStopList:
        await state.set_state(AdminMenuState.stop_list)
        return await bot.send_message(
            chat_id=call.from_user.id, text=content.text.list_is_empty(), reply_markup=content.inline.back_button(),
        )
    await bot.send_message(
        chat_id=call.from_user.id, text=content.text.choose_something(),
        reply_markup=content.inline.stop_list_keyboard(stop_list=stop_list),
    )


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


async def product_card(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
        ioc: InteractorFactory,
):
    data = await state.get_data()
    if call.data in ("back", "cancel_delete"):
        if data.get("admin_menu_product_id") is None:
            return await bot.send_message(chat_id=call.from_user.id, text=content.text.something_went_wrong())
    else:
        await state.update_data(admin_menu_product_id=int(call.data))
        data = await state.get_data()
    await read_product(call=call, bot=bot, content=content, data=data, ioc=ioc, state=state)


async def admin_edit_product_menu(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory,
):
    await call.message.delete()
    data = await state.get_data()
    read_product_case = await ioc.read_product_admin()
    product = await read_product_case(data=ReadProductDtoInput(menu_product_id=data.get("admin_menu_product_id")))
    await bot.send_message(
        chat_id=call.from_user.id, text=content.text.choose_something(),
        reply_markup=content.inline.product_edit_keyboard(
            mode=product.mode, price=[ProductPriceData(
                id=p.get("id"), price=p.get("price"), name=[],
            ) for p in data.get("product_price", [])],
        ),
    )


async def prepare_upload_photo_admin(
        call: types.CallbackQuery, bot: Bot, content: IContent,
):
    await call.message.delete()
    await bot.send_message(
        chat_id=call.from_user.id, text=content.text.upload_photo_text(),
        reply_markup=content.inline.back_button(),
    )


async def upload_photo_admin(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
        ioc: InteractorFactory, s3: S3Client,
):
    data = await state.get_data()
    file: types.File = await bot.get_file(file_id=message.photo[-1].file_id)
    photo_url = await send_file(file_path=file.file_path, s3=s3, token=bot.token)
    edit_photo_case = await ioc.edit_product_photo()
    await edit_photo_case(data=EditProductPhotoDtoInput(product_id=data.get("admin_product_id"), photo=photo_url))
    await read_product(call=message, bot=bot, content=content, data=data, ioc=ioc, state=state)


async def prepare_upload_name_admin(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await call.message.delete()
    data = await state.get_data()
    selected_language = get_not_exist_language(text=[ProductNameData(**n) for n in data.get("product_name", [])])
    await state.update_data(product_write_language_edit=selected_language)
    if selected_language is None:
        name: list[ProductNameData] = []
        selected_language = get_not_exist_language(text=name)
        await state.update_data(
            product_write_language_edit=selected_language,
            product_name=name,
        )
    await bot.send_message(
        chat_id=call.from_user.id, text=content.text.upload_name_text(language=selected_language),
        reply_markup=content.inline.back_button(),
    )


async def upload_name_admin(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
        states: AdminMenuState | StopListState, ioc: InteractorFactory,
):
    data = await state.get_data()
    product_name = data.get("product_name", [])
    name = ProductNameData(name=message.text, language=data.get("product_write_language_edit"))
    product_name.append(name.model_dump())
    await state.update_data(product_name=product_name)
    selected_language = get_not_exist_language(text=[ProductNameData(**n) for n in product_name])
    if selected_language is None:
        edit_name_case = await ioc.edit_product_name()
        await edit_name_case(data=EditProductNameDtoInput(
            product_id=data.get("admin_product_id"), name=[
                ProductName(name=n.get("name"), language=n.get("language")) for n in product_name
            ]),
        )
        await read_product(call=message, bot=bot, content=content, data=data, ioc=ioc, state=state)
        await state.set_state(states.product)
    else:
        await state.update_data(product_write_language_edit=selected_language)
        await bot.send_message(
            chat_id=message.from_user.id, text=content.text.upload_name_text(language=selected_language),
            reply_markup=content.inline.back_button(),
        )


async def prepare_upload_description_admin(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await call.message.delete()
    data = await state.get_data()
    selected_language = get_not_exist_language(
        text=[ProductDescriptionData(**d) for d in data.get("product_description", [])])
    await state.update_data(product_write_language_edit=selected_language)
    if selected_language is None:
        description = []
        selected_language = get_not_exist_language(text=description)
        await state.update_data(
            product_write_language_edit=selected_language,
            product_description=description,
        )
    await bot.send_message(
        chat_id=call.from_user.id, text=content.text.upload_description_text(language=selected_language),
        reply_markup=content.inline.back_button(),
    )


async def upload_description_admin(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
        states: AdminMenuState | StopListState, ioc: InteractorFactory,
):
    data = await state.get_data()
    product_description = data.get("product_description", [])
    description = ProductDescriptionData(description=message.text, language=data.get("product_write_language_edit"))
    product_description.append(description.model_dump())
    await state.update_data(product_description=product_description)
    selected_language = get_not_exist_language(text=[ProductDescriptionData(**n) for n in product_description])
    if selected_language is None:
        edit_description_case = await ioc.edit_product_description()
        await edit_description_case(data=EditProductDescriptionDtoInput(
            product_id=data.get("admin_product_id"), description=[
                ProductDescription(description=n.get("description"), language=n.get("language"))
                for n in product_description
            ]),
        )
        await read_product(call=message, bot=bot, content=content, data=data, ioc=ioc, state=state)
        await state.set_state(states.product)
    else:
        await state.update_data(product_write_language_edit=selected_language)
        await bot.send_message(
            chat_id=message.from_user.id, text=content.text.upload_name_text(language=selected_language),
            reply_markup=content.inline.back_button(),
        )


async def prepare_upload_default_price_admin(
        call: types.CallbackQuery, bot: Bot, content: IContent,
):
    await call.message.delete()
    await bot.send_message(chat_id=call.from_user.id, text=content.text.upload_price_text(),
                           reply_markup=content.inline.back_button())


async def upload_default_price_admin(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory,
):
    data = await state.get_data()
    read_product_case = await ioc.read_product_admin()
    product = await read_product_case(data=ReadProductDtoInput(menu_product_id=data.get("admin_menu_product_id")))
    edit_price_case = await ioc.edit_product_price()
    try:
        price = int(message.text)
    except ValueError:
        return await bot.send_message(chat_id=message.from_user.id, text=content.text.price_must_be_integer())
    await edit_price_case(
        data=EditProductPriceDtoInput(
            product_id=product.id, price=[ProductPrice(name=[], price=price)],
        ))
    await read_product(call=message, bot=bot, content=content, data=data, ioc=ioc, state=state)


async def prepare_upload_extend_price_admin(
        call: types.CallbackQuery, bot: Bot, content: IContent,
):
    await call.message.delete()
    await bot.send_message(chat_id=call.from_user.id, text=content.text.upload_price_text(),
                           reply_markup=content.inline.back_button())


async def upload_extend_price_admin(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
):
    data = await state.get_data()
    data["price_kind_edit"] = data.get("price_kind_edit", -1) + 1
    selected_price = data.get("price_kind_edit", 0)
    try:
        price = int(message.text)
    except ValueError:
        return await bot.send_message(chat_id=message.from_user.id, text=content.text.price_must_be_integer())
    if len(data.get("product_price", [])) == 0:
        data["product_price"] = [ProductPriceData(id=selected_price, price=price, name=[]).model_dump()]
    else:
        data.get("product_price").append(
            ProductPriceData(id=selected_price, price=price, name=[]).model_dump())
    selected_language = get_not_exist_language(
        text=[ProductPriceNameData.model_validate(i) for i in data.get("product_price")[selected_price].get("name")]
    )
    await state.update_data(
        product_write_language_edit=selected_language, product_price=data.get("product_price"),
        price_kind_edit=selected_price,
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text=content.text.upload_price_name_text(language=selected_language)
    )


async def upload_price_name_admin(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
        ioc: InteractorFactory, states: StopListState | AdminMenuState,
):
    data = await state.get_data()
    price_name = ProductPriceNameData(name=message.text, language=data.get("product_write_language_edit"))
    selected_price = data.get("price_kind_edit", 0)
    data.get("product_price")[selected_price].get("name").append(price_name.model_dump())
    await state.update_data(product_price=data.get("product_price"))
    selected_language = get_not_exist_language(
        text=[ProductPriceNameData.model_validate(i) for i in data.get("product_price")[selected_price].get("name")]
    )
    if selected_language is None:
        read_product_case = await ioc.read_product_admin()
        product = await read_product_case(data=ReadProductDtoInput(menu_product_id=data.get("admin_menu_product_id")))
        await bot.send_message(
            chat_id=message.from_user.id, text=content.text.choose_something(),
            reply_markup=content.inline.product_edit_keyboard(
                mode=product.mode, price=[ProductPriceData.model_validate(p) for p in data.get("product_price", [])],
            ),
        )
        await state.set_state(states.edit_product)
    else:
        await state.update_data(product_write_language_edit=selected_language)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=content.text.upload_price_name_text(language=selected_language),
        )


async def remove_price_admin(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory
):
    data = await state.get_data()
    product_price = data.get("product_price", [])
    for price in product_price:
        price_validated = ProductPriceData.model_validate(price)
        if price_validated.id == int(call.data.split("_")[2]):
            product_price.remove(price)
    await state.update_data(product_price=data.get("product_price"), price_kind_edit=len(data.get("product_price")) - 1)
    read_product_case = await ioc.read_product_admin()
    product = await read_product_case(data=ReadProductDtoInput(menu_product_id=data.get("admin_menu_product_id")))
    await call.message.delete()
    await bot.send_message(
        chat_id=call.from_user.id, text=content.text.choose_something(),
        reply_markup=content.inline.product_edit_keyboard(
            mode=product.mode, price=[ProductPriceData.model_validate(p) for p in data.get("product_price", [])],
        ),
    )


async def accept_update_price_admin(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext, ioc: InteractorFactory,
):
    data = await state.get_data()
    read_product_case = await ioc.read_product_admin()
    product = await read_product_case(data=ReadProductDtoInput(menu_product_id=data.get("admin_menu_product_id")))
    edit_price_case = await ioc.edit_product_price()
    await edit_price_case(data=EditProductPriceDtoInput(product_id=product.id, price=[
        ProductPrice(
            name=[ProductPriceName(name=n.get("name"), language=n.get("language")) for n in pr.get("name")],
            price=pr.get("price")) for pr in data.get("product_price")
    ]))
    await read_product(call=call, bot=bot, content=content, data=data, ioc=ioc, state=state)


async def change_menu_product_status_admin(
        call: types.CallbackQuery, bot: Bot, content: IContent,
        state: FSMContext, ioc: InteractorFactory,
) -> MenuProductStatus:
    data = await state.get_data()
    change_available_case = await ioc.edit_product_available()
    current_status = await change_available_case(
        data=EditProductAvailableDtoInput(menu_product_id=data.get("admin_menu_product_id")))
    read_product_case = await ioc.read_product_admin()
    product = await read_product_case(data=ReadProductDtoInput(menu_product_id=data.get("admin_menu_product_id")))
    with suppress(TelegramBadRequest):
        await bot.edit_message_reply_markup(
            chat_id=call.from_user.id, message_id=call.message.message_id,
            reply_markup=content.inline.product_admin_keyboard(menu_product_status=product.menu_product_status),
        )
    return current_status.status


async def remove_product_stop_list_admin(
        call: types.CallbackQuery, bot: Bot, content: IContent,
):
    await call.message.delete()
    await bot.send_message(
        chat_id=call.from_user.id, text=content.text.access_delete_product(),
        reply_markup=content.inline.access_delete_product_keyboard(),
    )


async def accept_delete_product_admin_from_stop_list(
        call: types.CallbackQuery, bot: Bot, content: IContent, ioc: InteractorFactory,
        state: FSMContext, user: User,
):
    data = await state.get_data()
    delete_product_case = await ioc.delete_product_from_system()
    await delete_product_case(data=DeleteProductDtoInput(product_id=data.get("admin_product_id")))
    await show_stop_list_by_restaurant_location_admin(
        call=call, bot=bot, content=content, state=state, ioc=ioc, user=user,
    )


async def accept_delete_product_admin_from_menu(
        call: types.CallbackQuery, bot: Bot, content: IContent, ioc: InteractorFactory,
        state: FSMContext, user: User,
):
    data = await state.get_data()
    delete_product_case = await ioc.delete_product_from_system()
    await delete_product_case(data=DeleteProductDtoInput(product_id=data.get("admin_product_id")))
    await get_category_products_admin(call=call, bot=bot, content=content, state=state, ioc=ioc, user=user)
