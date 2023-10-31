from src.application.common.use_case import UseCase
from src.application.read_user_addresses.dto import GetUserAddressesDtoInput, GetUserAddressesDtoOutput
from src.application.read_user_addresses.interfaces import DbGateway


class ReadUserAddressesCase(UseCase[GetUserAddressesDtoInput, GetUserAddressesDtoOutput]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: GetUserAddressesDtoInput) -> GetUserAddressesDtoOutput:
        addresses = await self.db_gateway.read_user_addresses(user_id=data.user_id)

        return GetUserAddressesDtoOutput(addresses=[
            address for address in addresses
        ])
