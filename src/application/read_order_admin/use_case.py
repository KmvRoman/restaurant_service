from src.application.common.exceptions import AdminOrderNotFound
from src.application.common.use_case import UseCase
from src.application.read_order_admin.dto import ReadAdminOrderDtoInput, ReadAdminOrderDtoOutput
from src.application.read_order_admin.interfaces import DbGateway


class ReadOrderAdminCase(UseCase[ReadAdminOrderDtoInput, ReadAdminOrderDtoOutput]):
    def __init__(self, db_gateway: DbGateway):
        self.db_gateway = db_gateway

    async def __call__(self, data: ReadAdminOrderDtoInput) -> ReadAdminOrderDtoOutput:
        order = await self.db_gateway.read_order_admin(order_id=data.order_id)
        if order is None:
            raise AdminOrderNotFound
        products = await self.db_gateway.read_admin_order_product(order_id=data.order_id, language=data.language)
        order.products = products
        return ReadAdminOrderDtoOutput(
            order_id=order.order_id, products=order.products,
            name=order.name, phone=order.phone, payment_type=order.payment_type, address=order.address,
            comment=order.comment, location=order.location, shipping_amount=order.shipping_amount,
            total_cost=order.total_cost,
        )
