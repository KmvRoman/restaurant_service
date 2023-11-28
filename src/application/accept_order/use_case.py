from src.application.accept_order.dto import AcceptOrderDtoInput, AcceptOrderDtoOutput
from src.application.accept_order.interfaces import DbGateway
from src.application.common.exceptions import OrderNotFound
from src.application.common.use_case import UseCase
from src.domain.order.services.order import OrderService
from src.domain.user.entities.user import UserId


class AcceptOrderCase(UseCase[AcceptOrderDtoInput, AcceptOrderDtoOutput]):
    def __init__(self, db_gateway: DbGateway, order_service: OrderService):
        self.db_gateway = db_gateway
        self.order_service = order_service

    async def __call__(self, data: AcceptOrderDtoInput) -> AcceptOrderDtoOutput:
        order = await self.db_gateway.exist_order(order_id=data.order_id)
        if order is None:
            raise OrderNotFound
        user_id = await self.db_gateway.accept_order(order_id=data.order_id)
        await self.db_gateway.commit()
        return AcceptOrderDtoOutput(user_id=UserId(int(user_id)))
