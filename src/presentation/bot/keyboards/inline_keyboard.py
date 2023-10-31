from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic import BaseModel

from src.domain.order.entities.order import OrderId
from src.presentation.bot.content.text_content.keyboard_content.inline.interfaces import (
    InlineButton, DefaultInlineButton, UrlInlineButton,
)


class InlineKeyboard:
    def restaurant_info(self, buttons: list[InlineButton]) -> InlineKeyboardMarkup:
        inline_buttons = []
        for button in buttons:
            if isinstance(button, DefaultInlineButton):
                inline_buttons.append([InlineKeyboardButton(text=button.text, callback_data=button.callback_data)])
            elif isinstance(button, UrlInlineButton):
                inline_buttons.append([InlineKeyboardButton(text=button.text, url=button.url)])
        return InlineKeyboardMarkup(inline_keyboard=inline_buttons)

    def user_settings(self, buttons: list[DefaultInlineButton]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=button.text, callback_data=button.callback_data)]
            for button in buttons
        ])

    def single_back_button(self, button: DefaultInlineButton) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=button.text, callback_data=button.callback_data)],
        ])

    def single_accept_button(self, button: DefaultInlineButton) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=button.text, callback_data=button.callback_data)],
        ])

    def change_language(self, buttons: list[DefaultInlineButton]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=button.text, callback_data=button.callback_data) for button in buttons],
        ])

    def categories(self, buttons: list[DefaultInlineButton]) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.adjust(2, 1)
        for button in buttons:
            builder.add(InlineKeyboardButton(text=button.text, callback_data=button.callback_data))
        return InlineKeyboardMarkup(inline_keyboard=builder.export())

    def upload_product_markup(self, buttons: list[DefaultInlineButton]) -> InlineKeyboardMarkup:
        inline_keyboard = []
        for button in buttons:
            if isinstance(button, list):
                price = []
                for b in button:
                    price.append(InlineKeyboardButton(text=b.text, callback_data=b.callback_data))
                inline_keyboard.append(price)
            else:
                inline_keyboard.append(
                    [InlineKeyboardButton(text=button.text, callback_data=button.callback_data)],
                )
        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    def choose_product_mode_markup(self, buttons: list[DefaultInlineButton]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text=button.text, callback_data=button.callback_data,
            )] for button in buttons
        ])

    def choose_branch(self, buttons: list[DefaultInlineButton]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=button.text, callback_data=button.callback_data)]
            for button in buttons
        ])

    def choose_menu(self, buttons: list[DefaultInlineButton]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=button.text, callback_data=button.callback_data)] for button in buttons
        ])

    def category_products(self, buttons: list[DefaultInlineButton]) -> InlineKeyboardMarkup:
        inline_buttons = []
        for button in buttons:
            if len(inline_buttons) > 0 and len(inline_buttons[-1]) < 2:
                inline_buttons[-1].append(
                    InlineKeyboardButton(text=button.text, callback_data=button.callback_data)
                )
            else:
                inline_buttons.append([InlineKeyboardButton(text=button.text, callback_data=button.callback_data)])
        return InlineKeyboardMarkup(inline_keyboard=inline_buttons)

    def admin_product(self, buttons: list[list[DefaultInlineButton], DefaultInlineButton]) -> InlineKeyboardMarkup:
        inline_buttons = []
        for button in buttons:
            if not isinstance(button, DefaultInlineButton):
                inline_buttons.append([InlineKeyboardButton(
                    text=i.text, callback_data=i.callback_data,
                ) for i in button])
            else:
                inline_buttons.append([InlineKeyboardButton(
                    text=button.text, callback_data=button.callback_data,
                )])
        return InlineKeyboardMarkup(inline_keyboard=inline_buttons)

    def edit_product(self, buttons: list[DefaultInlineButton | list[DefaultInlineButton]]) -> InlineKeyboardMarkup:
        inline_buttons = []
        for button in buttons:
            if not isinstance(button, DefaultInlineButton):
                inline_buttons.append([
                    InlineKeyboardButton(text=b.text, callback_data=b.callback_data) for b in button
                ])
            else:
                inline_buttons.append([
                    InlineKeyboardButton(text=button.text, callback_data=button.callback_data)
                ])
        return InlineKeyboardMarkup(inline_keyboard=inline_buttons)

    def stop_list(self, buttons: list[DefaultInlineButton]) -> InlineKeyboardMarkup:
        inline_buttons = []
        for button in buttons:
            if len(inline_buttons) == 0:
                inline_buttons.append([InlineKeyboardButton(text=button.text, callback_data=button.callback_data)])
            elif len(inline_buttons[-1]) < 2:
                inline_buttons[-1].append(InlineKeyboardButton(text=button.text, callback_data=button.callback_data))
            else:
                inline_buttons.append([InlineKeyboardButton(text=button.text, callback_data=button.callback_data)])
        return InlineKeyboardMarkup(inline_keyboard=inline_buttons)

    def delete_product_access(self, buttons: list[DefaultInlineButton]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=button.text, callback_data=button.callback_data) for button in buttons]
        ])

    def payment(self, button: DefaultInlineButton) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=button.text, callback_data=button.callback_data)],
        ])

    def accept_order_from_admin(self, button: DefaultInlineButton) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=button.text, callback_data=button.callback_data)]
        ])
