from typing import Optional, Any

from aiogram import Bot
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User

from src.infrastructure.database.repositories.user_repository import UserRepository
from src.presentation.bot.states.state_data.product import ProductData


class UploadExistPhotoFilter(Filter):
    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name

    async def __call__(
        self,
        message: Message,
        event_from_user: User,
        user_repo: UserRepository,
        bot: Bot, state: FSMContext
    ) -> bool | dict[str, Any]:
        data = await state.get_data()
        if data.get("product") is None:
            return False
        product = ProductData(**data.get("product"))
        if product.photo:
            return True
        return False


class UploadNotExistPhotoFilter(Filter):
    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name

    async def __call__(
        self,
        message: Message,
        event_from_user: User,
        user_repo: UserRepository,
        bot: Bot, state: FSMContext
    ) -> bool | dict[str, Any]:
        data = await state.get_data()
        if data.get("product") is None:
            return True
        product = ProductData(**data.get("product"))
        if product.photo is None:
            return True
        return False
