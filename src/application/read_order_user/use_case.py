from src.application.common.exceptions import UserOrderNotFound
from src.application.common.use_case import UseCase
from src.application.read_order_user.dto import ReadUserOrderDtoInput, ReadUserOrderDtoOutput
from src.application.read_order_user.interfaces import DbGateway


class ReadOrderUserCase(UseCase[ReadUserOrderDtoInput, ReadUserOrderDtoOutput]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: ReadUserOrderDtoInput) -> ReadUserOrderDtoOutput:
        order = await self.db_gateway.read_order_user(order_id=data.order_id, language=data.language)
        if order is None:
            raise UserOrderNotFound
        return ReadUserOrderDtoOutput(
            order_type=order.order_type, phone=order.phone, address=order.address,
            comment=order.comment, products=order.products, amount=order.amount,
            shipping_amount=order.shipping_amount, shipping_length=order.shipping_length,
            total_cost=order.total_cost,
        )
