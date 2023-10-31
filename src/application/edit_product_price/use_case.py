from src.application.common.use_case import UseCase
from src.application.edit_product_price.dto import EditProductPriceDtoInput
from src.application.edit_product_price.interfaces import DbGateway
from src.domain.product.services.product import ProductService


class EditProductPriceCase(UseCase[EditProductPriceDtoInput, None]):
    def __init__(self, db_gateway: DbGateway, product_service: ProductService):
        self.db_gateway = db_gateway
        self.product_service = product_service

    async def __call__(self, data: EditProductPriceDtoInput) -> None:
        product = await self.db_gateway.get_product_by_product_id(product_id=data.product_id)
        self.product_service.edit_product_price(price=data.price, product=product)
        await self.db_gateway.edit_product_price(price=product.price, product_id=product.id)
        await self.db_gateway.commit()
