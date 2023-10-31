from src.application.common.exceptions import UserNotExistError
from src.application.common.use_case import UseCase
from src.application.edit_user_name.dto import EditUserNameDtoInput
from src.application.edit_user_name.interfaces import DbGateway
from src.domain.user.services.user import UserService


class EditUserNameCase(UseCase[EditUserNameDtoInput, None]):
    def __init__(self, db_gateway: DbGateway, user_service: UserService):
        self.db_gateway = db_gateway
        self.user_service = user_service

    async def __call__(self, data: EditUserNameDtoInput) -> None:
        self.user_service.edit_user_name(name=data.name, user=data.user)
        await self.db_gateway.edit_user_name(name=data.user.name, user_id=data.user.id)
        await self.db_gateway.commit()
