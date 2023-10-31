from src.application.common.exceptions import UserNotExistError
from src.application.common.use_case import UseCase
from src.application.edit_user_phone.dto import UpdateUserPhoneDtoInput
from src.application.edit_user_phone.interfaces import DbGateway
from src.domain.user.services.user import UserService


class UpdateUserPhoneCase(UseCase[UpdateUserPhoneDtoInput, None]):
    def __init__(self, db_gateway: DbGateway, user_service: UserService):
        self.db_gateway = db_gateway
        self.user_service = user_service

    async def __call__(self, data: UpdateUserPhoneDtoInput) -> None:
        self.user_service.edit_phone(phone=data.phone, user=data.user)
        await self.db_gateway.edit_user_phone(phone=data.user.phone, user_id=data.user.id)
        await self.db_gateway.commit()
