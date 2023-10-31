from aiogram.types import Location

from src.application.common.exceptions import RestaurantLocationNotFound
from src.application.common.use_case import UseCase
from src.application.read_restaurant_location.dto import ReadLocationDtoInput, ReadLocationDtoOutput
from src.application.read_restaurant_location.interfaces import DbGateway


class ReadRestaurantLocationCase(UseCase[ReadLocationDtoInput, ReadLocationDtoOutput]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: ReadLocationDtoInput) -> ReadLocationDtoOutput:
        restaurant_location = await self.db_gateway.read_restaurant_location(location_id=data.location_id)
        if restaurant_location is None:
            raise RestaurantLocationNotFound
        return ReadLocationDtoOutput(
            address=restaurant_location.address,
            location=Location(
                longitude=restaurant_location.longitude, latitude=restaurant_location.latitude,
            )
        )
