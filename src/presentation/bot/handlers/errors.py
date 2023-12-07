from aiogram import Router, Bot, types
from aiogram.filters.exception import ExceptionTypeFilter

from src.application.common.exceptions import CurrentBasketNotFound
from src.presentation.bot.content.fasade.interfaces import IContent

error_catcher = Router(name="ErrorCatcher")


@error_catcher.error(ExceptionTypeFilter(CurrentBasketNotFound))
async def catch_empty_current_basket(update: types.ErrorEvent, bot: Bot, content: IContent):
    await bot.send_message(chat_id=update.update.message.from_user.id, text=content.text.empty_basket_error())


@error_catcher.error()
async def catch_empty_current_basket(update: types.ErrorEvent, bot: Bot, content: IContent):
    await bot.send_message(chat_id=update.update.message.from_user.id, text=content.text.critical_error())
