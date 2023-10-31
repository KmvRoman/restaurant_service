from src.application.common.use_case import UseCase
from src.application.read_restaurant_addresses.dto import (
    ReadRestaurantAddressesDtoInput, ReadRestaurantAddressesDtoOutput,
)
from src.application.read_restaurant_addresses.interfaces import DbGateway


class ReadRestaurantAddressesCase(UseCase[ReadRestaurantAddressesDtoInput, ReadRestaurantAddressesDtoOutput]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: ReadRestaurantAddressesDtoInput) -> ReadRestaurantAddressesDtoOutput:
        addresses = await self.db_gateway.read_restaurant_addresses(restaurant_id=data.restaurant_id)
        return ReadRestaurantAddressesDtoOutput(addresses=[
            address for address in addresses
        ])
