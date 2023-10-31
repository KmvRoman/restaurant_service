from src.application.common.use_case import UseCase
from src.application.edit_product_available.dto import EditProductAvailableDtoInput, EditProductAvailableDtoOutput
from src.application.edit_product_available.interfaces import DbGateway
from src.domain.restaurant.services.restaurant_location import RestaurantService


class EditProductAvailableCase(UseCase[EditProductAvailableDtoInput, EditProductAvailableDtoOutput]):
    def __init__(self, db_gateway: DbGateway, restaurant_service: RestaurantService):
        self.db_gateway = db_gateway
        self.restaurant_service = restaurant_service

    async def __call__(self, data: EditProductAvailableDtoInput) -> EditProductAvailableDtoOutput:
        menu_product = await self.db_gateway.get_product_location(menu_product_id=data.menu_product_id)
        self.restaurant_service.change_available_status(menu_product=menu_product)
        await self.db_gateway.edit_product_available(menu_product_id=data.menu_product_id, status=menu_product.status)
        await self.db_gateway.commit()
        return EditProductAvailableDtoOutput(status=menu_product.status)
