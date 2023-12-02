from aiogram.types import InlineKeyboardMarkup

from src.application.read_branches.dto import ReadBranchesDtoOutput
from src.application.read_detached_branches.dto import ReadDetachedBranchDtoOutput
from src.application.read_restaurants.dto import ReadRestaurantDtoOutput
from src.domain.order.entities.order import OrderId
from src.domain.user.constants.user import Language
from src.presentation.bot.content.text_content.keyboard_content.inline.interfaces import (
    IInlineKeyboardText, UrlInlineButton, DefaultInlineButton,
)
from src.presentation.bot.keyboards.inline_keyboard import InlineKeyboard


class UzbekInlineKeyboardText(IInlineKeyboardText):
    language = Language.uz

    def __init__(self, inline_keyboard: InlineKeyboard):
        self.inline_keyboard = inline_keyboard

    async def restaurant_info_keyboard(
            self, restaurant_addresses: list[ReadRestaurantDtoOutput],
    ) -> InlineKeyboardMarkup:
        result = [UrlInlineButton(text="Instagram", url="https://instagram.com/roma1998_1")]
        for loc in restaurant_addresses:
            result.append(DefaultInlineButton(text=f"📍 {loc.address}", callback_data=str(loc.id)))
        return self.inline_keyboard.restaurant_info(buttons=result)

    def user_settings_keyboard(self) -> InlineKeyboardMarkup:
        buttons = [
            DefaultInlineButton(text="Ismini ozgartirish", callback_data="change_name"),
            DefaultInlineButton(text="Nomerini ozgartirish", callback_data="change_phone"),
            DefaultInlineButton(text="Tilini ozgartirish", callback_data="change_language"),
        ]
        return self.inline_keyboard.user_settings(buttons=buttons)

    def back_button(self) -> InlineKeyboardMarkup:
        button = DefaultInlineButton(text="⬅ Ortga", callback_data="back")
        return self.inline_keyboard.single_back_button(button=button)

    def accept_button(self) -> InlineKeyboardMarkup:
        button = DefaultInlineButton(text="✅ Подтвердить", callback_data="accept")
        return self.inline_keyboard.single_accept_button(button=button)

    def change_language_keyboard(self) -> InlineKeyboardMarkup:
        buttons = [
            DefaultInlineButton(text="🇷🇺 ruscha", callback_data=Language.ru),
            DefaultInlineButton(text="🇺🇿 uzbekcha", callback_data=Language.uz)
        ]
        keyboard = self.inline_keyboard.change_language(buttons=buttons)
        keyboard.inline_keyboard.extend(self.back_button().inline_keyboard)
        return keyboard

    def payment_keyboard(self, payment_url: str) -> InlineKeyboardMarkup:
        button = DefaultInlineButton(text="Оплатить", callback_data="pay")
        keyboard = self.inline_keyboard.payment(button=button)
        keyboard.inline_keyboard.extend(self.back_button().inline_keyboard)
        return keyboard

    def accept_order_admin_keyboard_pickup(self, order_id: OrderId) -> InlineKeyboardMarkup:
        return self.inline_keyboard.accept_order_from_admin(
            button=DefaultInlineButton(text="☑️ Подтвердить", callback_data=f"adp_{order_id}"),
        )

    def accepted_order_admin_keyboard_pickup(self) -> InlineKeyboardMarkup:
        return self.inline_keyboard.accept_order_from_admin(
            button=DefaultInlineButton(text="✅ Подтверждено", callback_data=f"..."),
        )

    def accept_order_admin_keyboard_shipping(self, order_id: OrderId) -> InlineKeyboardMarkup:
        return self.inline_keyboard.accept_order_from_admin(
            button=DefaultInlineButton(text="☑️ Подтвердить", callback_data=f"adsh_{order_id}"),
        )

    def accepted_order_admin_keyboard_shipping(self) -> InlineKeyboardMarkup:
        return self.inline_keyboard.accept_order_from_admin(
            button=DefaultInlineButton(text="✅ Подтверждено", callback_data=f"..."),
        )

    def groups_match_with_branches(self, buttons: list[ReadDetachedBranchDtoOutput]) -> InlineKeyboardMarkup:
        pass
