from typing import Optional, Any

from aiogram import Bot
from aiogram.filters import Filter
from aiogram.types import Message, User

from src.infrastructure.database.repositories.user_repository import UserRepository


class CurrentRestaurant(Filter):
    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name

    async def __call__(
        self,
        message: Message,
        event_from_user: User,
        user_repo: UserRepository,
        bot: Bot,
    ) -> bool | dict[str, Any]:
        restaurant_id = await user_repo.get_restaurant(token=bot.token)
        data = {"restaurant": restaurant_id}
        if restaurant_id is None:
            return False
        return data
