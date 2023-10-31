from dataclasses import dataclass

from src.domain.order.constants.order import PaymentType
from src.domain.order.entities.order import OrderId


@dataclass
class ChoosePaymentMethodDtoInput:
    order_id: OrderId
    payment_type: PaymentType
