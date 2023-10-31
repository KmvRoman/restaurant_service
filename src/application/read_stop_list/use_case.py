from src.application.common.exceptions import EmptyStopList
from src.application.common.use_case import UseCase
from src.application.read_stop_list.dto import ReadStopListDtoInput, ReadStopListDtoOutput
from src.application.read_stop_list.interfaces import DbGateway


class ReadStopListCase(UseCase[ReadStopListDtoInput, ReadStopListDtoOutput]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: ReadStopListDtoInput) -> list[ReadStopListDtoOutput]:
        stop_list = await self.db_gateway.read_stop_list(location_id=data.location_id, language=data.language)
        if stop_list is None:
            raise EmptyStopList
        response_stop_list = []
        for st in stop_list:
            response_stop_list.append(ReadStopListDtoOutput(menu_product_id=st.menu_product_id, name=st.name))
        return response_stop_list
