from src.application.common.use_case import UseCase
from src.application.edit_product_description.dto import EditProductDescriptionDtoInput
from src.application.edit_product_description.interfaces import DbGateway
from src.domain.product.services.product import ProductService


class EditProductDescriptionCase(UseCase[EditProductDescriptionDtoInput, None]):
    def __init__(self, db_gateway: DbGateway, product_service: ProductService):
        self.db_gateway = db_gateway
        self.product_service = product_service

    async def __call__(self, data: EditProductDescriptionDtoInput) -> None:
        product = await self.db_gateway.get_product_by_product_id(product_id=data.product_id)
        if len(product.description) == 0:
            self.product_service.edit_product_description(description=data.description, product=product)
            await self.db_gateway.add_product_description(description=product.description, product_id=product.id)
        else:
            self.product_service.edit_product_description(description=data.description, product=product)
            await self.db_gateway.edit_product_description(description=product.description, product_id=product.id)
        await self.db_gateway.commit()
