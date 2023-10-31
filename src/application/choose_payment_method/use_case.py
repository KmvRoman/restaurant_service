from src.application.choose_payment_method.dto import ChoosePaymentMethodDtoInput
from src.application.choose_payment_method.interfaces import DbGateway
from src.application.common.exceptions import OrderNotFound
from src.application.common.use_case import UseCase
from src.domain.order.services.order import OrderService


class ChoosePaymentMethodCase(UseCase[ChoosePaymentMethodDtoInput, None]):
    def __init__(self, db_gateway: DbGateway, order_service: OrderService):
        self.db_gateway = db_gateway
        self.order_service = order_service

    async def __call__(self, data: ChoosePaymentMethodDtoInput) -> None:
        order = await self.db_gateway.get_order(order_id=data.order_id)
        if order is None:
            raise OrderNotFound
        self.order_service.choose_payment_method(order=order, payment_type=data.payment_type)
        await self.db_gateway.choose_payment_method(order=order)
