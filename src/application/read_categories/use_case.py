from src.application.common.use_case import UseCase
from src.application.read_categories.dto import ReadCategoriesDtoInput, ReadCategoriesDtoOutput
from src.application.read_categories.interfaces import DbGateway


class ReadCategoriesCase(UseCase[ReadCategoriesDtoInput, ReadCategoriesDtoOutput]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: ReadCategoriesDtoInput) -> ReadCategoriesDtoOutput:
        categories = await self.db_gateway.read_categories(restaurant_id=data.restaurant_id, language=data.language)
        return ReadCategoriesDtoOutput(categories=categories)
