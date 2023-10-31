from src.application.common.use_case import UseCase
from src.application.create_user.dto import CreateUserDtoInput, CreateUserDtoOutput
from src.application.create_user.interfaces import DbGateway
from src.domain.user.services.user import UserService


class CreateUserUseCase(UseCase[CreateUserDtoInput, CreateUserDtoOutput]):
    def __init__(self, db_gateway: DbGateway, user_service: UserService):
        self.db_gateway = db_gateway
        self.user_service = user_service

    async def __call__(self, data: CreateUserDtoInput) -> CreateUserDtoOutput:
        user = self.user_service.create_user(
            name=data.name, phone=data.phone, language=data.language, member=data.member,
        )
        user_id = await self.db_gateway.create_user(user=user)
        return CreateUserDtoOutput(user_id=user_id)
