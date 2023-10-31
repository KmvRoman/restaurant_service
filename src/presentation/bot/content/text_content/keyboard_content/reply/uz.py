from aiogram.types import ReplyKeyboardMarkup

from src.application.read_restaurant_addresses.dto import ReadRestaurantAddressesDtoOutput
from src.application.read_user_addresses.dto import GetUserAddressesDtoOutput
from src.domain.order.constants.order import OrderType
from src.domain.order.entities.order import Location
from src.domain.restaurant.entities.restaurant_view import RestaurantId
from src.domain.user.constants.user import Language
from src.domain.user.entities.user import UserId
from src.presentation.bot.content.text_content.keyboard_content.reply.enums import MainMenuUz, HomeUz, BackUz, \
    ChooseOrderTypeUz, SendLocationUz, WebAppUz, SkipUz, MyPhoneNumberUz, AcceptUz, PaymentTypesUz
from src.presentation.bot.content.text_content.keyboard_content.reply.interfaces import IReplyKeyboardText
from src.presentation.bot.keyboards.reply_keyboard import ReplyKeyboard


class UzbekReplyKeyboardText(IReplyKeyboardText):
    language = Language.uz

    def __init__(self, reply_keyboard: ReplyKeyboard):
        self.reply_keyboard = reply_keyboard

    def users_main_menu(self) -> ReplyKeyboardMarkup:
        return self.reply_keyboard.users_main_menu(buttons=MainMenuUz)

    def main_menu_button(self) -> ReplyKeyboardMarkup:
        return self.reply_keyboard.main_menu_button(buttons=HomeUz)

    def back_button(self) -> ReplyKeyboardMarkup:
        return self.reply_keyboard.back_button(button=BackUz)

    def choose_order_type_keyboard(self) -> ReplyKeyboardMarkup:
        keyboard = self.reply_keyboard.choose_order_type(buttons=ChooseOrderTypeUz)
        keyboard.keyboard.extend(self.back_button().keyboard)
        return keyboard

    def send_location_shipping(self, payload: GetUserAddressesDtoOutput) -> ReplyKeyboardMarkup:
        addresses = [button for button in payload.addresses]
        buttons = [SendLocationUz.location]
        buttons.extend(addresses)
        return self.reply_keyboard.send_location(buttons=buttons)

    def send_location_pickup(self, payload: ReadRestaurantAddressesDtoOutput) -> ReplyKeyboardMarkup:
        addresses = [button for button in payload.addresses]
        buttons = [SendLocationUz.location]
        buttons.extend(addresses)
        keyboard = self.reply_keyboard.send_location(buttons=buttons)
        keyboard.keyboard.extend(self.back_button().keyboard)
        return keyboard

    def webapp_input_keyboard(
            self, user_id: UserId, restaurant_id: RestaurantId,
            user_location: Location | None, language: Language, restaurant_location_id: int,
            order_type: OrderType,
    ) -> ReplyKeyboardMarkup:
        keyboard = self.reply_keyboard.webapp_menu(
            button=WebAppUz, user_id=user_id, restaurant_id=restaurant_id,
            user_location=user_location, language=language, restaurant_location_id=restaurant_location_id,
            order_type=order_type,
        )
        keyboard.keyboard.extend(self.back_button().keyboard)
        return keyboard

    def user_comment_keyboard(self) -> ReplyKeyboardMarkup:
        keyboard = self.reply_keyboard.skip_button(button=SkipUz)
        keyboard.keyboard.extend(self.back_button().keyboard)
        return keyboard

    def user_phone_number_keyboard(self) -> ReplyKeyboardMarkup:
        keyboard = self.reply_keyboard.phone_number(button=MyPhoneNumberUz)
        keyboard.keyboard.extend(self.back_button().keyboard)
        return keyboard

    def user_accept_order_keyboard(self) -> ReplyKeyboardMarkup:
        keyboard = self.reply_keyboard.accept_order(button=AcceptUz)
        keyboard.keyboard.extend(self.back_button().keyboard)
        return keyboard

    def payment_type_choose(self) -> ReplyKeyboardMarkup:
        keyboard = self.reply_keyboard.payment_type(buttons=PaymentTypesUz)
        keyboard.keyboard.extend(self.back_button().keyboard)
        return keyboard
