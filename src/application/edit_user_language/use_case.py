from src.application.common.use_case import UseCase
from src.application.edit_user_language.dto import UpdateUserLanguageDtoInput
from src.application.edit_user_language.interfaces import DbGateway
from src.domain.user.services.user import UserService


class UpdateUserLanguageCase(UseCase[UpdateUserLanguageDtoInput, None]):
    def __init__(self, db_gateway: DbGateway, user_service: UserService):
        self.db_gateway = db_gateway
        self.user_service = user_service

    async def __call__(self, data: UpdateUserLanguageDtoInput) -> None:
        self.user_service.edit_language(language=data.language, user=data.user)
        await self.db_gateway.edit_user_language(language=data.user.language, user_id=data.user.id)
        await self.db_gateway.commit()
