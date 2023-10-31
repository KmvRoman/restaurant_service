from typing import Optional, Any

from aiogram.filters import Filter
from aiogram.types import Message, User

from src.application.create_user.dto import CreateUserDtoInput
from src.domain.user.constants.user import Member, Language
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.presentation.bot.content.get_implement import LanguageManager


class CreateUserFilter(Filter):
    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name

    async def __call__(
        self,
        message: Message,
        event_from_user: User,
        ioc: InteractorFactory,
        user_repo: UserRepository,
        content: LanguageManager,
    ) -> bool | dict[str, Any]:
        user = await user_repo.get_user_by_telegram_id(telegram_id=event_from_user.id)
        data = {"user": user}
        if user is None:
            create_user = await ioc.create_user()
            user_id = await create_user(data=CreateUserDtoInput(
                name=event_from_user.first_name, phone=None,
                language=Language(event_from_user.language_code),
                member=Member.user,
            ))
            await user_repo.create_telegram_user(user_id=user_id.user_id, telegram_id=event_from_user.id)
            user = await user_repo.get_user_by_user_id(user_id=user_id.user_id)
            data["user"] = user
        else:
            data["user"] = user
        if user.member == Member.administrator:
            data["content"] = content(language=Language.ru)
        else:
            data["content"] = content(language=user.language)
        return data
