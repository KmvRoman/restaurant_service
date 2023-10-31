from src.application.common.use_case import UseCase
from src.application.read_branches.dto import ReadBranchesDtoInput, ReadBranchesDtoOutput
from src.application.read_branches.interfaces import DbGateway


class ReadRestaurantBranchesCase(UseCase[ReadBranchesDtoInput, ReadBranchesDtoOutput]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: ReadBranchesDtoInput) -> list[ReadBranchesDtoOutput]:
        branches = await self.db_gateway.read_branches(restaurant_id=data.restaurant_id)
        return [
            ReadBranchesDtoOutput(location_id=br.location_id, address=br.address) for br in branches
        ]
