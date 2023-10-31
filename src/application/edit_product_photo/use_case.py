from src.application.common.use_case import UseCase
from src.application.edit_product_photo.dto import EditProductPhotoDtoInput
from src.application.edit_product_photo.interfaces import DbGateway
from src.domain.product.services.product import ProductService


class EditProductPhotoCase(UseCase[EditProductPhotoDtoInput, None]):
    def __init__(self, db_gateway: DbGateway, product_service: ProductService):
        self.db_gateway = db_gateway
        self.product_service = product_service

    async def __call__(self, data: EditProductPhotoDtoInput) -> None:
        product = await self.db_gateway.get_product_by_product_id(product_id=data.product_id)
        if product.photo is None:
            self.product_service.edit_product_photo(photo=data.photo, product=product)
            await self.db_gateway.add_product_photo(photo=product.photo, product_id=product.id)
        else:
            self.product_service.edit_product_photo(photo=data.photo, product=product)
            await self.db_gateway.edit_product_photo(photo=product.photo, product_id=product.id)
        await self.db_gateway.commit()
