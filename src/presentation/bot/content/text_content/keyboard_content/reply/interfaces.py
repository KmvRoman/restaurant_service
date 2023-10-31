from typing import Protocol

from aiogram.types import ReplyKeyboardMarkup

from src.application.read_restaurant_addresses.dto import ReadRestaurantAddressesDtoOutput
from src.application.read_user_addresses.dto import GetUserAddressesDtoOutput
from src.domain.order.constants.order import OrderType
from src.domain.order.entities.order import Location
from src.domain.restaurant.entities.restaurant_view import RestaurantId
from src.domain.user.constants.user import Language
from src.domain.user.entities.user import UserId


class IReplyKeyboardText(Protocol):
    language: Language

    def users_main_menu(self) -> ReplyKeyboardMarkup:
        raise NotImplementedError

    def main_menu_button(self) -> ReplyKeyboardMarkup:
        raise NotImplementedError

    def administrators_main_menu(self) -> ReplyKeyboardMarkup:
        raise NotImplementedError

    def administrator_home(self) -> ReplyKeyboardMarkup:
        raise NotImplementedError

    def choose_order_type_keyboard(self) -> ReplyKeyboardMarkup:
        raise NotImplementedError

    def send_location_shipping(self, payload: GetUserAddressesDtoOutput) -> ReplyKeyboardMarkup:
        raise NotImplementedError

    def send_location_pickup(self, payload: ReadRestaurantAddressesDtoOutput) -> ReplyKeyboardMarkup:
        raise NotImplementedError

    def webapp_input_keyboard(
            self, user_id: UserId, restaurant_id: RestaurantId,
            user_location: Location | None, language: Language, restaurant_location_id: int,
            order_type: OrderType,
    ) -> ReplyKeyboardMarkup:
        raise NotImplementedError

    def webapp_back_keyboard(
            self, user_id: UserId, restaurant_id: RestaurantId,
            user_location: Location | None, language: Language, restaurant_location_id: int,
            order_type: OrderType,
    ) -> ReplyKeyboardMarkup:
        raise NotImplementedError

    def user_comment_keyboard(self) -> ReplyKeyboardMarkup:
        raise NotImplementedError

    def user_phone_number_keyboard(self) -> ReplyKeyboardMarkup:
        raise NotImplementedError

    def user_accept_order_keyboard(self) -> ReplyKeyboardMarkup:
        raise NotImplementedError

    def payment_type_choose(self) -> ReplyKeyboardMarkup:
        raise NotImplementedError
