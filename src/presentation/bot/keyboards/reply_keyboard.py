from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

from src.domain.order.constants.order import OrderType
from src.domain.order.entities.order import Location
from src.domain.restaurant.entities.restaurant_view import RestaurantId
from src.domain.user.constants.user import Language
from src.domain.user.entities.user import UserId
from src.infrastructure.config.common import CommunicationAddress
from src.presentation.bot.content.text_content.keyboard_content.reply.enums import (
    MainMenu, Home, AdminMainMenu, AdminHome, ChooseOrderType, Back, WebApp, MyPhoneNumber, Skip, Accept, PaymentTypes,
)


class ReplyKeyboard:
    def users_main_menu(self, buttons: type[MainMenu]) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text=buttons.menu)],
            [KeyboardButton(text=buttons.info), KeyboardButton(text=buttons.review)],
            [KeyboardButton(text=buttons.settings)],
        ])

    def main_menu_button(self, buttons: type[Home]) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text=buttons.home)],
        ])

    def back_button(self, button: type[Back]) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text=button.back)]])

    def admins_main_menu(self, buttons: type[AdminMainMenu]) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text=buttons.menu)],
            [KeyboardButton(text=buttons.newsletter), KeyboardButton(text=buttons.upload_product)],
            [KeyboardButton(text=buttons.statistic), KeyboardButton(text=buttons.promotion)],
        ])

    def administrator_home(self, buttons: type[AdminHome]) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text=buttons.home)]
        ])

    def choose_order_type(self, buttons: type[ChooseOrderType]) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text=buttons.pickup), KeyboardButton(text=buttons.shipping)]
        ])

    def send_location(self, buttons: list[str]) -> ReplyKeyboardMarkup:
        reply_buttons = []
        for count, button in enumerate(buttons):
            if count == 0:
                reply_buttons.append([KeyboardButton(text=button, request_location=True)])
            else:
                reply_buttons.append([KeyboardButton(text=button)])
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=reply_buttons)

    def webapp_menu(
            self, button: type[WebApp], user_id: UserId, restaurant_id: RestaurantId,
            user_location: Location | None, language: Language, restaurant_location_id: int,
            order_type: OrderType,) -> ReplyKeyboardMarkup:
        if user_location is None:
            return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
                [KeyboardButton(web_app=WebAppInfo(
                    url=f"{CommunicationAddress.frontend}/?user_id={user_id}&restaurant_id={restaurant_id}&"
                        f"&user_language={language}&restaurant_location_id={restaurant_location_id}&"
                        f"order_type={order_type}"
                ), text=button.webapp)]
            ])
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(web_app=WebAppInfo(
                url=f"{CommunicationAddress.frontend}/?user_id={user_id}&restaurant_id={restaurant_id}&"
                    f"latitude={user_location.latitude}&longitude={user_location.longitude}&user_language={language}&"
                    f"restaurant_location_id={restaurant_location_id}&order_type={order_type}"
            ), text=button.webapp)]
        ])

    def skip_button(self, button: type[Skip]) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text=button.skip)]
        ])

    def phone_number(self, button: type[MyPhoneNumber]) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text=button.phone, request_contact=True)]
        ])

    def accept_order(self, button: type[Accept]) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text=button.accept)]
        ])

    def payment_type(self, buttons: type[PaymentTypes]) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text=buttons.cache)],
            [KeyboardButton(text=buttons.payme)],
            [KeyboardButton(text=buttons.click)],
        ])
