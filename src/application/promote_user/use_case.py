from src.application.common.exceptions import UserNotExistError
from src.application.common.use_case import UseCase
from src.application.promote_user.dto import PromoteUserDtoInput
from src.application.promote_user.interfaces import DbGateway
from src.domain.user.services.user import UserService


class PromoteUserCase(UseCase[PromoteUserDtoInput, None]):
    def __init__(self, db_gateway: DbGateway, user_service: UserService):
        self.db_gateway = db_gateway
        self.user_service = user_service

    async def __call__(self, data: PromoteUserDtoInput) -> None:
        user = await self.db_gateway.get_user_by_user_id(user_id=data.user_id)
        if user is None:
            raise UserNotExistError
        self.user_service.promote_user(member=data.member, user=user)
        await self.db_gateway.promote_user(member=user.member, user_id=user.id)
        await self.db_gateway.commit()
