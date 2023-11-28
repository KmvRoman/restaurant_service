from src.application.common.exceptions import UserOrderNotFound
from src.application.common.use_case import UseCase
from src.application.read_order_user.dto import ReadUserOrderDtoInput, ReadUserOrderDtoOutput
from src.application.read_order_user.interfaces import DbGateway


class ReadOrderUserCase(UseCase[ReadUserOrderDtoInput, ReadUserOrderDtoOutput]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: ReadUserOrderDtoInput) -> ReadUserOrderDtoOutput:
        order = await self.db_gateway.read_order_user(order_id=data.order_id)
        if order is None:
            raise UserOrderNotFound
        products = await self.db_gateway.read_user_order_product(order_id=data.order_id, language=data.language)
        order.products = products
        return ReadUserOrderDtoOutput(
            order_id=order.order_id, products=order.products,
            amount=order.amount, total_cost=order.total_cost,
        )
