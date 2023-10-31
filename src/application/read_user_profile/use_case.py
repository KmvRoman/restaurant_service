from src.application.common.exceptions import UserNotExistError
from src.application.common.use_case import UseCase
from src.application.read_user_profile.dto import ReadUserProfileDtoInput, ReadUserProfileDtoOutput
from src.application.read_user_profile.interfaces import DbGateway


class ReadUserProfileCase(UseCase[ReadUserProfileDtoInput, ReadUserProfileDtoOutput]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: ReadUserProfileDtoInput) -> ReadUserProfileDtoOutput:
        user = await self.db_gateway.get_user_by_user_id(user_id=data.user_id)
        if user is None:
            raise UserNotExistError
        return ReadUserProfileDtoOutput(
            user_id=user.id, name=user.name, phone=user.phone,
            member=user.member, language=user.language,
        )
