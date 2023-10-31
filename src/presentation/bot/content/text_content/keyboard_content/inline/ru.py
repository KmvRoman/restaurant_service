from aiogram.types import InlineKeyboardMarkup

from src.application.read_branches.dto import ReadBranchesDtoOutput
from src.application.read_category_products.dto import CategoryProduct
from src.application.read_stop_list.dto import ReadStopListDtoOutput
from src.domain.order.entities.order import OrderId
from src.domain.product.constants.product import ProductMode
from src.domain.restaurant.constants.constants import MenuProductStatus
from src.domain.restaurant.entities.restaurant_view import RestaurantId, Category
from src.domain.user.constants.user import Language
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.presentation.bot.content.text_content.keyboard_content.inline.interfaces import (
    IInlineKeyboardText, DefaultInlineButton, UrlInlineButton,
)
from src.presentation.bot.keyboards.inline_keyboard import InlineKeyboard
from src.presentation.bot.states.state_data.product import ProductPriceData


class RussianInlineKeyboardText(IInlineKeyboardText):
    language = Language.ru

    def __init__(self, user_repo: UserRepository, inline_keyboard: InlineKeyboard):
        self.user_repo = user_repo
        self.inline_keyboard = inline_keyboard

    async def restaurant_info_keyboard(
            self, restaurant_id: RestaurantId,
    ) -> InlineKeyboardMarkup:
        locations = await self.user_repo.read_restaurant_locations(restaurant_id=restaurant_id)
        result = [UrlInlineButton(text="Instagram", url="https://instagram.com/roma1998_1")]
        for loc in locations:
            result.append(DefaultInlineButton(text=f"📍 {loc.address}", callback_data=str(loc.id)))
        return self.inline_keyboard.restaurant_info(buttons=result)

    def user_settings_keyboard(self) -> InlineKeyboardMarkup:
        buttons = [
            DefaultInlineButton(text="Изменить Ф.И.О.", callback_data="change_name"),
            DefaultInlineButton(text="Изменить номер", callback_data="change_phone"),
            DefaultInlineButton(text="Изменить язык", callback_data="change_language"),
        ]
        return self.inline_keyboard.user_settings(buttons=buttons)

    def back_button(self) -> InlineKeyboardMarkup:
        button = DefaultInlineButton(text="⬅ Назад", callback_data="back")
        return self.inline_keyboard.single_back_button(button=button)

    def accept_button(self) -> InlineKeyboardMarkup:
        button = DefaultInlineButton(text="✅ Подтвердить", callback_data="accept")
        return self.inline_keyboard.single_accept_button(button=button)

    def change_language_keyboard(self) -> InlineKeyboardMarkup:
        buttons = [
            DefaultInlineButton(text="🇷🇺 русский", callback_data=Language.ru),
            DefaultInlineButton(text="🇺🇿 узбекский", callback_data=Language.uz)
        ]
        keyboard = self.inline_keyboard.change_language(buttons=buttons)
        keyboard.inline_keyboard.extend(self.back_button().inline_keyboard)
        return keyboard

    def categories_keyboard(self, buttons: list[Category]) -> InlineKeyboardMarkup:
        keyboard = self.inline_keyboard.categories(buttons=[
            DefaultInlineButton(text=button.category, callback_data=str(button.id))
            for button in buttons
        ])
        return keyboard

    def admin_menu_categories_keyboard(self, buttons: list[Category]) -> InlineKeyboardMarkup:
        keyboard = self.inline_keyboard.categories(buttons=[
            DefaultInlineButton(text=button.category, callback_data=str(button.id))
            for button in buttons
        ])
        keyboard.inline_keyboard.extend(self.back_button().inline_keyboard)
        return keyboard

    def uploading_product_process_keyboard(
            self, photo: bool, name: bool, description: bool,
            price: list[ProductPriceData], mode: ProductMode | None,
    ) -> InlineKeyboardMarkup:
        buttons = [
            DefaultInlineButton(text="☑️ Фото" if photo else "Фото", callback_data="upload_photo"),
            DefaultInlineButton(text="☑️ Название" if name else "Название", callback_data="upload_name"),
            DefaultInlineButton(
                text="☑️ Описание" if description else "Описание",
                callback_data="upload_description"
            ),
        ]
        if len(price) > 0:
            new_price_list: list[ProductPriceData] = sorted(price, key=lambda x: x.id)
            for pr in new_price_list:
                buttons.append(
                    [
                        DefaultInlineButton(
                            text=str(pr.price), callback_data=str(pr.id),
                        ),
                        DefaultInlineButton(text="➖", callback_data=f"remove_price_{pr.id}")
                    ]
                )
        if mode is None and len(price) == 0:
            buttons.append(DefaultInlineButton(text="Цена ➕", callback_data="upload_price"))
        elif mode == ProductMode.default and len(price) == 0:
            buttons.append(DefaultInlineButton(text="Цена ➕", callback_data="upload_default_price"))
        elif mode == ProductMode.extend and len(price) > 0:
            buttons.append(DefaultInlineButton(text="Цена ➕", callback_data="upload_extend_price"))
        keyboard = self.inline_keyboard.upload_product_markup(buttons=buttons)
        keyboard.inline_keyboard.extend(self.accept_button().inline_keyboard)
        keyboard.inline_keyboard.extend(self.back_button().inline_keyboard)
        return keyboard

    def choose_product_mode(self) -> InlineKeyboardMarkup:
        buttons = [
            DefaultInlineButton(text="Обычный(одна модицификация)", callback_data="default"),
            DefaultInlineButton(text="Расширенный", callback_data="extend"),
        ]
        keyboard = self.inline_keyboard.choose_product_mode_markup(buttons=buttons)
        keyboard.inline_keyboard.extend(self.back_button().inline_keyboard)
        return keyboard

    def choose_branch(self, branches: list[ReadBranchesDtoOutput]) -> InlineKeyboardMarkup:
        buttons = [
            DefaultInlineButton(text=br.address, callback_data=str(br.location_id)) for br in branches
        ]

        return self.inline_keyboard.choose_branch(buttons=buttons)

    def choose_menu_keyboard(self) -> InlineKeyboardMarkup:
        buttons = [
            DefaultInlineButton(text="🍽 Всё меню", callback_data="menu_admin"),
            DefaultInlineButton(text="⛔ Стоп-лист", callback_data="stop_list")
        ]
        keyboard = self.inline_keyboard.choose_menu(buttons=buttons)
        keyboard.inline_keyboard.extend(self.back_button().inline_keyboard)
        return keyboard

    def category_products_keyboard(self, products: list[CategoryProduct]) -> InlineKeyboardMarkup:
        buttons = [
            DefaultInlineButton(text=pr.name, callback_data=str(pr.menu_product_id))
            for pr in products]
        keyboard = self.inline_keyboard.category_products(buttons=buttons)
        keyboard.inline_keyboard.append(self.back_button().inline_keyboard[0])
        return keyboard

    def product_admin_keyboard(
            self, menu_product_status: MenuProductStatus,
    ) -> InlineKeyboardMarkup:
        buttons = [
            [DefaultInlineButton(text="✖️ Удалить", callback_data="remove_product"),
             DefaultInlineButton(text="🔨 Изменить", callback_data="edit_product")],
        ]
        if menu_product_status == MenuProductStatus.available:
            buttons.append(DefaultInlineButton(text="✅ Есть в наличии", callback_data="not_available"))
        else:
            buttons.append(DefaultInlineButton(text="⛔️ Нет в наличии", callback_data="available"))
        keyboard = self.inline_keyboard.admin_product(buttons=buttons)
        keyboard.inline_keyboard.extend(self.back_button().inline_keyboard)
        return keyboard

    def product_edit_keyboard(self, mode: ProductMode, price: list[ProductPriceData]) -> InlineKeyboardMarkup:
        buttons = [
            DefaultInlineButton(text="Изменить фото", callback_data="change_photo"),
            DefaultInlineButton(text="Изменить имя", callback_data="change_name"),
            DefaultInlineButton(text="Изменить описание", callback_data="change_description"),
        ]
        if len(price) > 0:
            new_price_list: list[ProductPriceData] = sorted(price, key=lambda x: x.id)
            for pr in new_price_list:
                buttons.append(
                    [
                        DefaultInlineButton(
                            text=str(pr.price), callback_data=str(pr.id),
                        ),
                        DefaultInlineButton(text="➖", callback_data=f"remove_price_{pr.id}")
                    ]
                )
        if mode == ProductMode.default and len(price) == 0:
            buttons.append(DefaultInlineButton(text="Изменить цену", callback_data="change_default_price"))
        elif mode == ProductMode.extend and len(price) >= 0:
            buttons.append(DefaultInlineButton(text="Цена ➕", callback_data="change_extend_price"))
        if mode == ProductMode.extend and len(price) > 1:
            buttons.append(DefaultInlineButton(text="✅ Подтвердить", callback_data="accept"))
        keyboard = self.inline_keyboard.edit_product(buttons=buttons)
        keyboard.inline_keyboard.extend(self.back_button().inline_keyboard)
        return keyboard

    def stop_list_keyboard(self, stop_list: list[ReadStopListDtoOutput]) -> InlineKeyboardMarkup:
        buttons = []
        for pr in stop_list:
            buttons.append(DefaultInlineButton(text=f"⛔️ {pr.name}", callback_data=str(pr.menu_product_id)))
        keyboard = self.inline_keyboard.stop_list(buttons=buttons)
        keyboard.inline_keyboard.extend(self.back_button().inline_keyboard)
        return keyboard

    def access_delete_product_keyboard(self) -> InlineKeyboardMarkup:
        buttons = [
            DefaultInlineButton(text="✅ Да", callback_data="accept"),
            DefaultInlineButton(text="❌ Отменить", callback_data="cancel_delete"),
        ]
        keyboard = self.inline_keyboard.delete_product_access(buttons=buttons)
        keyboard.inline_keyboard.extend(self.back_button().inline_keyboard)
        return keyboard

    def payment_keyboard(self, payment_url: str) -> InlineKeyboardMarkup:
        button = DefaultInlineButton(text="Оплатить", callback_data="pay")
        keyboard = self.inline_keyboard.payment(button=button)
        keyboard.inline_keyboard.extend(self.back_button().inline_keyboard)
        return keyboard

    def accept_order_admin_keyboard_pickup(self, order_id: OrderId) -> InlineKeyboardMarkup:
        return self.inline_keyboard.accept_order_from_admin(
            button=DefaultInlineButton(text="✅ Подтвердить", callback_data=f"adp_{order_id}"),
        )
