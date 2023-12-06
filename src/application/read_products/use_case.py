from src.application.common.exceptions import ProductNotExistError, RestaurantLocationsNotFound
from src.application.common.use_case import UseCase
from src.application.read_products.dto import ReadProductsDtoInput, ReadProductsDtoOutput
from src.application.read_products.interfaces import DbGateway
from src.domain.restaurant.services.restaurant_location import RestaurantService


class ReadProductsCase(UseCase[ReadProductsDtoInput, ReadProductsDtoOutput]):
    def __init__(self, db_gateway: DbGateway, restaurant_service: RestaurantService):
        self.db_gateway = db_gateway
        self.restaurant_service = restaurant_service

    async def __call__(self, data: ReadProductsDtoInput) -> list[ReadProductsDtoOutput]:
        locations = await self.db_gateway.read_restaurant_locations(restaurant_id=data.restaurant_id)
        if locations is None:
            raise RestaurantLocationsNotFound
        nearest_restaurant_location = self.restaurant_service.get_nearest_restaurant(
            user_location=data.user_location, restaurants_locations=locations,
        )
        products = await self.db_gateway.read_products(
            location_id=nearest_restaurant_location.id, language=data.language,
        )
        if products is None:
            raise ProductNotExistError
        await self.db_gateway.close()
        return [
            ReadProductsDtoOutput(
                id=cat.id, category=cat.category,
                products=cat.products,
            ) for cat in products
        ]
