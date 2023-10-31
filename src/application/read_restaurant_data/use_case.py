from src.application.common.exceptions import RestaurantDataNotFound
from src.application.common.use_case import UseCase
from src.application.read_restaurant_data.dto import ReadRestaurantDataDtoInput, ReadRestaurantDataDtoOutput
from src.application.read_restaurant_data.interfaces import DbGateway


class ReadRestaurantDataCase(UseCase[ReadRestaurantDataDtoInput, ReadRestaurantDataDtoOutput]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: ReadRestaurantDataDtoInput) -> ReadRestaurantDataDtoOutput:
        restaurant_data = await self.db_gateway.read_restaurant_data(
            restaurant_id=data.restaurant_id, language=data.language,
        )
        if restaurant_data is None:
            raise RestaurantDataNotFound
        return ReadRestaurantDataDtoOutput(
            name=restaurant_data.name,
            description=restaurant_data.description,
            locations=restaurant_data.location,
        )
