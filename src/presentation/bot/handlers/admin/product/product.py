from aiogram import Router, Bot, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.application.create_product.dto import CreateProductDtoInput
from src.application.read_categories.dto import ReadCategoriesDtoInput
from src.domain.product.constants.product import ProductMode, ProductStatus
from src.domain.product.entities.product import ProductPrice, ProductPriceName, ProductName, ProductDescription
from src.domain.restaurant.entities.restaurant_view import RestaurantId, CategoryId
from src.domain.user.constants.user import Language
from src.domain.user.entities.user import User
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.infrastructure.web.s3.client import S3Client
from src.presentation.bot.content.fasade.interfaces import IContent
from src.presentation.bot.content.text_content.keyboard_content.reply.enums import AdminMainMenu
from src.presentation.bot.exceptions.common import (
    ValueNotInstanceCategoryId, NameNotFoundAnyLanguages, DescriptionNotFoundAnyLanguages,
    PriceNameNotFoundAnyLanguages, EmptyProductName, EmptyPriceError,
)
from src.presentation.bot.handlers.admin.product.send_file import send_file
from src.presentation.bot.states.admin.product import AddProductState
from src.presentation.bot.states.state_data.product import (
    ProductData, ProductNameData, ProductDescriptionData, ProductPriceNameData,
    ProductPriceData, ProductDataValidate,
)

product_router = Router()


def get_not_exist_language(
        text: list[
            ProductNameData |
            ProductDescriptionData |
            ProductPriceNameData
            ],
) -> Language | None:
    for language in list(Language):
        if language not in [text.language for text in text]:
            selected_language = Language(language)
            break
    else:
        selected_language = None
    if selected_language is None:
        return None
    return selected_language


async def send_menu_upload_product(
        bot: Bot, content: IContent,
        message: types.Message | types.CallbackQuery,
        state: FSMContext,
):
    if isinstance(message, types.CallbackQuery):
        await message.message.delete()
    data = await state.get_data()
    if data.get("product") is None:
        await state.update_data(product=ProductData().model_dump())
        data = await state.get_data()
        product = ProductData(**data.get("product"))
    else:
        product = ProductData(**data.get("product"))
    if product.photo:
        await bot.send_photo(
            chat_id=message.from_user.id, photo=product.photo, caption=content.text.uploading_product(
                photo=product.photo, name=product.name,
                description=product.description, price=product.price,
            ),
            reply_markup=content.inline.uploading_product_process_keyboard(
                photo=bool(product.photo), name=bool(product.name),
                description=bool(product.description), price=product.price, mode=product.mode,
            )
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id, text=content.text.uploading_product(
                photo=product.photo, name=product.name,
                description=product.description, price=product.price,
            ),
            reply_markup=content.inline.uploading_product_process_keyboard(
                photo=bool(product.photo), name=bool(product.name),
                description=bool(product.description), price=product.price, mode=product.mode,
            )
        )
    await state.set_state(AddProductState.menu_upload_product)


@product_router.callback_query(F.data == "back", AddProductState.menu_upload_product)
@product_router.message(F.text.in_([i.upload_product for i in AdminMainMenu.__subclasses__()]))
async def choose_category(
        message: types.Message, bot: Bot, ioc: InteractorFactory,
        content: IContent, state: FSMContext, restaurant: int, user: User,
):
    categories_data = await ioc.read_categories()
    categories = await categories_data(
        data=ReadCategoriesDtoInput(
            restaurant_id=RestaurantId(restaurant),
            language=user.language,
        )
    )
    if isinstance(message, types.CallbackQuery):
        await message.message.delete()
    else:
        await message.delete()
    data = await state.get_data()
    if data.get("home_in_product_add") is None:
        message_home = await bot.send_message(
            chat_id=message.from_user.id, text=content.text.choose_something(),
            reply_markup=content.reply.administrator_home(),
        )
        await state.update_data(home_in_product_add=message_home.message_id)
    await bot.send_message(
        chat_id=message.from_user.id, text=content.text.categories(),
        reply_markup=content.inline.categories_keyboard(buttons=categories.categories),
    )
    await state.set_state(AddProductState.menu)


@product_router.callback_query(
    F.data == "back",
    StateFilter(
        AddProductState.add_photo, AddProductState.add_name,
        AddProductState.add_description, AddProductState.select_mode,
        AddProductState.add_default_price, AddProductState.add_extend_price,
    )
)
@product_router.callback_query(AddProductState.menu)
async def start_upload_product(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await send_menu_upload_product(bot=bot, content=content, message=call, state=state)
    if call.data != "back":
        data = await state.get_data()
        product = ProductData(**data.get("product"))
        try:
            product.category_id = CategoryId(int(call.data))
        except ValueError:
            return await bot.send_message(chat_id=call.from_user.id, text=content.text.something_went_wrong())
        await state.update_data(product=product.model_dump())
    await state.set_state(AddProductState.menu_upload_product)
    await call.answer()


@product_router.callback_query(AddProductState.menu_upload_product, F.data == "upload_photo")
async def prepare_upload_photo(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await call.message.delete()
    await bot.send_message(
        chat_id=call.from_user.id, text=content.text.upload_photo_text(),
        reply_markup=content.inline.back_button(),
    )
    await state.set_state(AddProductState.add_photo)
    await call.answer()


@product_router.message(F.photo, AddProductState.add_photo)
async def upload_photo(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
):
    data = await state.get_data()
    product = ProductData(**data.get("product"))
    product.photo = message.photo[-1].file_id
    await state.update_data(product=product.model_dump())
    await send_menu_upload_product(bot=bot, content=content, message=message, state=state)
    await state.set_state(AddProductState.menu_upload_product)


@product_router.callback_query(AddProductState.menu_upload_product, F.data == "upload_name")
async def prepare_upload_name(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await call.message.delete()
    data = await state.get_data()
    product = ProductData(**data.get("product"))
    selected_language = get_not_exist_language(text=product.name)
    await state.update_data(product_write_language=selected_language)
    if selected_language is None:
        product.name = []
        selected_language = get_not_exist_language(text=product.name)
        await state.update_data(product_write_language=selected_language, product=product.model_dump())
    await bot.send_message(
        chat_id=call.from_user.id, text=content.text.upload_name_text(language=selected_language),
        reply_markup=content.inline.back_button(),
    )
    await state.set_state(AddProductState.add_name)
    await call.answer()


@product_router.message(AddProductState.add_name)
async def upload_name(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
):
    data = await state.get_data()
    product = ProductData(**data.get("product"))
    name = ProductNameData(name=message.text, language=data.get("product_write_language"))
    product.name.append(name)
    await state.update_data(product=product.model_dump())
    selected_language = get_not_exist_language(text=product.name)
    if selected_language is None:
        await send_menu_upload_product(bot=bot, content=content, message=message, state=state)
    else:
        await state.update_data(product_write_language=selected_language)
        await bot.send_message(
            chat_id=message.from_user.id, text=content.text.upload_name_text(language=selected_language),
            reply_markup=content.inline.back_button(),
        )


@product_router.callback_query(AddProductState.menu_upload_product, F.data == "upload_description")
async def prepare_upload_description(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await call.message.delete()
    data = await state.get_data()
    product = ProductData(**data.get("product"))
    selected_language = get_not_exist_language(text=product.description)
    await state.update_data(product_write_language=selected_language)
    if selected_language is None:
        product.description = []
        selected_language = get_not_exist_language(text=product.description)
        await state.update_data(product_write_language=selected_language, product=product.model_dump())
    await bot.send_message(
        chat_id=call.from_user.id, text=content.text.upload_description_text(language=selected_language),
        reply_markup=content.inline.back_button(),
    )
    await state.set_state(AddProductState.add_description)
    await call.answer()


@product_router.message(AddProductState.add_description)
async def upload_description(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
):
    data = await state.get_data()
    product = ProductData(**data.get("product"))
    description = ProductDescriptionData(description=message.text, language=data.get("product_write_language"))
    product.description.append(description)
    await state.update_data(product=product.model_dump())
    selected_language = get_not_exist_language(text=product.description)
    if selected_language is None:
        await send_menu_upload_product(bot=bot, content=content, message=message, state=state)
    else:
        await state.update_data(product_write_language=selected_language)
        await bot.send_message(
            chat_id=message.from_user.id, text=content.text.upload_description_text(language=selected_language),
            reply_markup=content.inline.back_button(),
        )


@product_router.callback_query(F.data == "upload_price", AddProductState.menu_upload_product)
async def select_default_mode(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await call.message.delete()
    await bot.send_message(chat_id=call.from_user.id, text=content.text.choose_mode(),
                           reply_markup=content.inline.choose_product_mode())
    await state.set_state(AddProductState.select_mode)
    await call.answer()


@product_router.callback_query(
    StateFilter(AddProductState.select_mode, AddProductState.menu_upload_product),
    F.data.in_(["default", "upload_default_price"]),
)
async def prepare_upload_price(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await call.message.delete()
    await bot.send_message(chat_id=call.from_user.id, text=content.text.upload_price_text(),
                           reply_markup=content.inline.back_button())
    await state.set_state(AddProductState.add_default_price)
    await call.answer()


@product_router.message(AddProductState.add_default_price)
async def upload_default_price(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
):
    data = await state.get_data()
    product = ProductData(**data.get("product"))
    try:
        product.price = [ProductPriceData(id=0, price=int(message.text), name=[])]
    except ValueError:
        return await bot.send_message(chat_id=message.from_user.id, text=content.text.price_must_be_integer())
    product.mode = ProductMode.default
    await state.update_data(product=product.model_dump())
    await send_menu_upload_product(bot=bot, content=content, message=message, state=state)


@product_router.callback_query(
    StateFilter(AddProductState.select_mode, AddProductState.menu_upload_product),
    F.data.in_(["extend", "upload_extend_price"]),
)
async def prepare_upload_price(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    await call.message.delete()
    await bot.send_message(chat_id=call.from_user.id, text=content.text.upload_price_text(),
                           reply_markup=content.inline.back_button())
    await state.set_state(AddProductState.add_extend_price)
    await call.answer()


@product_router.message(AddProductState.add_extend_price)
async def upload_price(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
):
    data = await state.get_data()
    data["price_kind"] = data.get("price_kind", -1) + 1
    product = ProductData(**data.get("product"))
    if product.mode is None:
        product.mode = ProductMode.extend
    selected_price = data.get("price_kind", 0)
    try:
        price = int(message.text)
    except ValueError:
        return await bot.send_message(chat_id=message.from_user.id, text=content.text.price_must_be_integer())
    if len(product.price) == 0:
        product.price = [ProductPriceData(id=selected_price, price=price, name=[])]
    else:
        product.price.append(ProductPriceData(id=selected_price, price=price, name=[]))
    selected_language = get_not_exist_language(text=product.price[selected_price].name)
    await state.update_data(
        product_write_language=selected_language, product=product.model_dump(),
        price_kind=selected_price,
    )
    await bot.send_message(
        chat_id=message.from_user.id,
        text=content.text.upload_price_name_text(language=selected_language)
    )
    await state.set_state(AddProductState.add_price_name)


@product_router.message(AddProductState.add_price_name)
async def upload_price_name(
        message: types.Message, bot: Bot, content: IContent, state: FSMContext,
):
    data = await state.get_data()
    product = ProductData(**data.get("product"))
    price_name = ProductPriceNameData(name=message.text, language=data.get("product_write_language"))
    selected_price = data.get("price_kind", 0)
    product.price[selected_price].name.append(price_name)
    await state.update_data(product=product.model_dump())
    selected_language = get_not_exist_language(text=product.price[selected_price].name)
    if selected_language is None:
        await send_menu_upload_product(bot=bot, content=content, message=message, state=state)
    else:
        await state.update_data(product_write_language=selected_language)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=content.text.upload_price_name_text(language=selected_language),
        )


@product_router.callback_query(F.data.startswith("remove_price"), AddProductState.menu_upload_product)
async def remove_price(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
):
    data = await state.get_data()
    product = ProductData(**data.get("product"))
    for price in product.price:
        if price.id == int(call.data.split("_")[2]):
            product.price.remove(price)
    if len(product.price) == 0:
        product.mode = None
    await state.update_data(product=product.model_dump(), price_kind=len(product.price) - 1)
    await send_menu_upload_product(bot=bot, content=content, message=call, state=state)
    await call.answer()


@product_router.callback_query(F.data == "accept", AddProductState.menu_upload_product)
async def add_product(
        call: types.CallbackQuery, bot: Bot, content: IContent, state: FSMContext,
        s3: S3Client, ioc: InteractorFactory, restaurant: RestaurantId,
):
    data = await state.get_data()
    product = ProductData(**data.get("product"))
    if product.photo is not None:
        file: types.File = await bot.get_file(file_id=product.photo)
        product.photo = await send_file(file_path=file.file_path, s3=s3, token=bot.token)
    try:
        product = ProductDataValidate(
            category_id=product.category_id, photo=product.photo,
            name=product.name, description=product.description,
            mode=product.mode, price=product.price,
            status=ProductStatus.active,
        )
    except ValueNotInstanceCategoryId:
        return await bot.send_message(
            chat_id=call.from_user.id, text=content.text.category_not_found_in_add_product())
    except (NameNotFoundAnyLanguages, EmptyProductName):
        return await bot.send_message(
            chat_id=call.from_user.id, text=content.text.name_not_found_in_add_product())
    except DescriptionNotFoundAnyLanguages:
        return await bot.send_message(
            chat_id=call.from_user.id, text=content.text.description_not_full())
    except EmptyPriceError:
        return await bot.send_message(
            chat_id=call.from_user.id, text=content.text.price_name_not_found_in_add_product())
    except PriceNameNotFoundAnyLanguages:
        return await bot.send_message(
            chat_id=call.from_user.id, text=content.text.price_is_empty())
    create_product_case = await ioc.create_product()
    await create_product_case(data=CreateProductDtoInput(
        restaurant_id=restaurant, category_id=product.category_id, photo=product.photo,
        name=[
            ProductName(name=n.name, language=n.language) for n in product.name
        ], description=[
            ProductDescription(description=d.description, language=d.language) for d in product.description
        ], mode=product.mode,
        price=[
            ProductPrice(name=[
                ProductPriceName(name=n.name, language=n.language) for n in pr.name
            ], price=pr.price) for pr in product.price
        ],
    ))
    await call.message.delete()
    await bot.send_message(chat_id=call.from_user.id, text=content.text.finish_create_product())
    await bot.send_message(
        chat_id=call.from_user.id, text=content.text.greeting_administrator(),
        reply_markup=content.reply.administrators_main_menu())
    await state.clear()
    await call.answer()
