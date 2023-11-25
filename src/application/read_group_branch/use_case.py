from src.application.common.exceptions import GroupIdCantBeNone
from src.application.common.use_case import UseCase
from src.application.read_group_branch.interface import DbGateway


class ReadBranchGroupCase(UseCase[int, int]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, restaurant_location_id: int) -> int:
        group_id = await self.db_gateway.read_branch_group(restaurant_location_id=restaurant_location_id)
        if group_id is None:
            raise GroupIdCantBeNone
        return group_id
