from src.application.common.exceptions import CategoryProductsIsEmpty
from src.application.common.use_case import UseCase
from src.application.read_category_products.dto import ReadCategoryProductsDtoInput, ReadCategoryDtoOutput, \
    CategoryProduct
from src.application.read_category_products.interfaces import DbGateway


class ReadCategoryProductsCase(UseCase[ReadCategoryProductsDtoInput, ReadCategoryDtoOutput]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: ReadCategoryProductsDtoInput) -> ReadCategoryDtoOutput:
        category_products = await self.db_gateway.read_category_products(
            location_id=data.location_id, language=data.language, category_id=data.category_id,
        )
        if category_products is None:
            raise CategoryProductsIsEmpty
        return ReadCategoryDtoOutput(
            category_name=category_products[0].category_name,
            products=[
                CategoryProduct(
                    menu_product_id=pr.menu_product_id,
                    name=pr.name,
                    menu_product_status=pr.menu_product_status
                ) for pr in category_products
            ])
