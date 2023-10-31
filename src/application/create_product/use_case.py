from src.application.common.use_case import UseCase
from src.application.create_product.dto import CreateProductDtoInput, CreateProductDtoOutput
from src.application.create_product.interfaces import DbGateway
from src.domain.product.constants.product import ProductStatus
from src.domain.product.services.product import ProductService


class CreateProductCase(UseCase[CreateProductDtoInput, CreateProductDtoOutput]):
    def __init__(self, db_gateway: DbGateway, product_service: ProductService):
        self.db_gateway = db_gateway
        self.product_service = product_service

    async def __call__(self, data: CreateProductDtoInput) -> CreateProductDtoOutput:
        product = self.product_service.create_product(
            photo=data.photo, name=data.name, description=data.description,
            mode=data.mode, price=data.price, status=ProductStatus.active,
        )
        locations_id = await self.db_gateway.read_restaurant_locations_id(restaurant_id=data.restaurant_id)
        product_id = await self.db_gateway.create_product(product=product)
        await self.db_gateway.create_menu_product(
            locations_id=locations_id, category_id=data.category_id, product_id=product_id,
        )
        await self.db_gateway.commit()
        return CreateProductDtoOutput(product_id=product_id)
