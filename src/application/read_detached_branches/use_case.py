from src.application.common.use_case import UseCase
from src.application.read_detached_branches.dto import ReadDetachedBranchesDtoInput, ReadDetachedBranchDtoOutput
from src.application.read_detached_branches.interfaces import DbGateway


class ReadDetachedBranchesCase(UseCase[ReadDetachedBranchesDtoInput, list[ReadDetachedBranchDtoOutput]]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: ReadDetachedBranchesDtoInput) -> list[ReadDetachedBranchDtoOutput]:
        branches = await self.db_gateway.read_detached_branches(restaurant_id=data.restaurant_id)
        return [
            ReadDetachedBranchDtoOutput(location_id=br.location_id, address=br.address) for br in branches
        ]
