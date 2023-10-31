from src.application.common.exceptions import UserLocationNotFound
from src.application.common.use_case import UseCase
from src.application.read_user_location_by_address.dto import ReadUserLocationByAddressDtoInput, \
    ReadUserLocationByAddressDtoOutput
from src.application.read_user_location_by_address.interfaces import DbGateway


class ReadUserLocationByAddressCase(UseCase[ReadUserLocationByAddressDtoInput, ReadUserLocationByAddressDtoOutput]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: ReadUserLocationByAddressDtoInput) -> ReadUserLocationByAddressDtoOutput:
        location = await self.db_gateway.read_user_location_by_address(address=data.address, user_id=data.user_id)
        if location is None:
            raise UserLocationNotFound
        return ReadUserLocationByAddressDtoOutput(location=location)
