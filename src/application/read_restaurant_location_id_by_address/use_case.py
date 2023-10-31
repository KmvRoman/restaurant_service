from src.application.common.exceptions import RestaurantLocationIdNotFound
from src.application.common.use_case import UseCase
from src.application.read_restaurant_location_id_by_address.dto import ReadRestaurantLocationIdByAddressDtoInput, \
    ReadRestaurantLocationIdByAddressDtoOutput
from src.application.read_restaurant_location_id_by_address.interfaces import DbGateway


class ReadRestaurantLocationIdByAddressCase(
    UseCase[ReadRestaurantLocationIdByAddressDtoInput, ReadRestaurantLocationIdByAddressDtoOutput]
):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(
            self, data: ReadRestaurantLocationIdByAddressDtoInput,
    ) -> ReadRestaurantLocationIdByAddressDtoOutput:
        location_id = await self.db_gateway.read_restaurant_location_id_by_address(
            restaurant_id=data.restaurant_id, address=data.address)
        if location_id is None:
            raise RestaurantLocationIdNotFound
        return ReadRestaurantLocationIdByAddressDtoOutput(location_id=location_id)
