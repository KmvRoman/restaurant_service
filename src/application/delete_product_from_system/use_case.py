from src.application.common.use_case import UseCase
from src.application.delete_product_from_system.dto import DeleteProductDtoInput
from src.application.delete_product_from_system.interfaces import DbGateway
from src.domain.product.services.product import ProductService


class DeleteProductCase(UseCase[DeleteProductDtoInput, None]):
    def __init__(self, db_gateway: DbGateway, product_service: ProductService):
        self.db_gateway = db_gateway
        self.product_service = product_service

    async def __call__(self, data: DeleteProductDtoInput) -> None:
        product = await self.db_gateway.get_product_by_product_id(product_id=data.product_id)
        self.product_service.delete_product(product=product)
        await self.db_gateway.delete_product(product_id=product.id)
        await self.db_gateway.commit()
