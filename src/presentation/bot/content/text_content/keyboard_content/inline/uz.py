from aiogram.types import InlineKeyboardMarkup

from src.domain.order.entities.order import OrderId
from src.domain.restaurant.entities.restaurant_view import RestaurantId, Category
from src.domain.user.constants.user import Language
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.presentation.bot.content.text_content.keyboard_content.inline.interfaces import (
    IInlineKeyboardText, UrlInlineButton, DefaultInlineButton,
)
from src.presentation.bot.keyboards.inline_keyboard import InlineKeyboard


class UzbekInlineKeyboardText(IInlineKeyboardText):
    language = Language.uz

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

    def accept_order_admin_keyboard(self, order_id: OrderId) -> InlineKeyboardMarkup:
        return self.inline_keyboard.accept_order_from_admin(
            button=DefaultInlineButton(text="✅ Подтвердить", callback_data=f"adac_{order_id}"),
        )
