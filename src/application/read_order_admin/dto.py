from dataclasses import dataclass
from typing import Optional

from src.domain.order.constants.order import OrderType, PaymentType
from src.domain.order.entities.order import OrderId, Location
from src.domain.order.entities.order_view import ReadAdminOrderProduct
from src.domain.user.constants.user import Language


@dataclass
class ReadAdminOrderDtoInput:
    order_id: OrderId
    language: Language


@dataclass
class ReadAdminOrderDtoOutput:
    order_id: OrderId
    products: list[ReadAdminOrderProduct]
    name: str
    phone: str
    payment_type: PaymentType
    address: Optional[str]
    comment: Optional[str]
    location: Optional[Location]
    shipping_amount: Optional[str]
    total_cost: int
