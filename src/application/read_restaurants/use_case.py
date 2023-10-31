from src.application.common.exceptions import RestaurantsNotFound
from src.application.common.use_case import UseCase
from src.application.read_restaurants.dto import ReadRestaurantsDtoInput, ReadRestaurantDtoOutput
from src.application.read_restaurants.interfaces import DbGateway


class ReadRestaurantsLocationsCase(UseCase[ReadRestaurantsDtoInput, ReadRestaurantDtoOutput]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: ReadRestaurantsDtoInput) -> list[ReadRestaurantDtoOutput]:
        restaurants = await self.db_gateway.read_restaurant_locations(restaurant_id=data.restaurant_id)
        if restaurants is None or len(restaurants) == 0:
            raise RestaurantsNotFound
        rests = []
        for restaurant in restaurants:
            rests.append(
                ReadRestaurantDtoOutput(
                    id=restaurant.id, address=restaurant.address,
                    latitude=restaurant.latitude, longitude=restaurant.longitude,
                )
            )
        return rests
