from dataclasses import dataclass
from typing import Protocol

from aiogram.types import InlineKeyboardMarkup

from src.application.read_branches.dto import ReadBranchesDtoOutput
from src.application.read_category_products.dto import CategoryProduct
from src.application.read_restaurants.dto import ReadRestaurantDtoOutput
from src.application.read_stop_list.dto import ReadStopListDtoOutput
from src.domain.order.entities.order import OrderId
from src.domain.product.constants.product import ProductMode
from src.domain.restaurant.constants.constants import MenuProductStatus
from src.domain.restaurant.entities.restaurant_view import RestaurantId, Category, RestaurantLocation
from src.domain.user.constants.user import Language
from src.presentation.bot.states.state_data.product import ProductPriceData


@dataclass
class InlineButton:
    text: str


@dataclass
class DefaultInlineButton(InlineButton):
    callback_data: str


@dataclass
class UrlInlineButton(InlineButton):
    url: str


class IInlineKeyboardText(Protocol):
    language: Language

    async def restaurant_info_keyboard(
            self, restaurant_addresses: list[ReadRestaurantDtoOutput],
    ) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def back_button(self) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def accept_button(self) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def basket_keyboard(self) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def user_settings_keyboard(self) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def change_language_keyboard(self) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def categories_keyboard(self, buttons: list[Category]) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def admin_menu_categories_keyboard(self, buttons: list[Category]) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def uploading_product_process_keyboard(
            self, photo: bool, name: bool, description: bool,
            price: list[ProductPriceData], mode: ProductMode,
    ) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def choose_product_mode(self) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def choose_branch(self, branches: list[ReadBranchesDtoOutput]) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def choose_menu_keyboard(self) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def category_products_keyboard(self, products: list[CategoryProduct]) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def product_admin_keyboard(
            self, menu_product_status: MenuProductStatus,
    ) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def product_edit_keyboard(
            self, mode: ProductMode, price: list[ProductPriceData],
    ) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def stop_list_keyboard(self, stop_list: list[ReadStopListDtoOutput]) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def access_delete_product_keyboard(self) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def payment_keyboard(self, payment_url: str) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def accept_order_admin_keyboard_pickup(self, order_id: OrderId) -> InlineKeyboardMarkup:
        raise NotImplementedError

    def accept_order_admin_keyboard_shipping(self, order_id: OrderId) -> InlineKeyboardMarkup:
        raise NotImplementedError
