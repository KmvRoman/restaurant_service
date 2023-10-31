from src.application.common.exceptions import ProductNotFound
from src.application.common.use_case import UseCase
from src.application.read_product_admin.dto import ReadProductDtoInput, ReadProductDtoOutput
from src.application.read_product_admin.interfaces import DbGateway


class ReadProductAdminCase(UseCase[ReadProductDtoInput, ReadProductDtoOutput]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: ReadProductDtoInput) -> ReadProductDtoOutput:
        product = await self.db_gateway.get_product_by_menu_product_id(menu_product_id=data.menu_product_id)
        if product is None:
            raise ProductNotFound
        return ReadProductDtoOutput(
            id=product.id, photo=product.photo, name=product.name, description=product.description,
            mode=product.mode, price=product.price, product_status=product.product_status,
            menu_product_status=product.menu_product_status,
        )
