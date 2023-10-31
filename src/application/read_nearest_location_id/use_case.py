from src.application.common.exceptions import RestaurantLocationsNotFound
from src.application.common.use_case import UseCase
from src.application.read_nearest_location_id.dto import ReadNearestLocationDtoInput, ReadNearestLocationDtoOutput
from src.application.read_nearest_location_id.interfaces import DbGateway
from src.domain.restaurant.services.restaurant_location import RestaurantService


class ReadNearestRestaurantLocation(UseCase[ReadNearestLocationDtoInput, ReadNearestLocationDtoOutput]):
    def __init__(self, db_gateway: DbGateway, restaurant_service: RestaurantService):
        self.db_gateway = db_gateway
        self.restaurant_service = restaurant_service

    async def __call__(self, data: ReadNearestLocationDtoInput) -> ReadNearestLocationDtoOutput:
        locations = await self.db_gateway.read_restaurant_locations(restaurant_id=data.restaurant_id)
        if locations is None:
            raise RestaurantLocationsNotFound
        nearest_restaurant_location = self.restaurant_service.get_nearest_restaurant(
            user_location=data.user_location, restaurants_locations=locations,
        )
        return ReadNearestLocationDtoOutput(
            address=nearest_restaurant_location.address,
            restaurant_location_id=nearest_restaurant_location.id,
        )
