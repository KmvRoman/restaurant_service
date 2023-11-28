from typing import NamedTuple, Optional

from src.domain.order.constants.order import PaymentType
from src.domain.order.entities.order import OrderId


class AdminOrderShow(NamedTuple):
    order_id: OrderId
    name: str
    phone: str
    payment_type: PaymentType
    address: Optional[str]
    comment: Optional[str]
    longitude: float
    latitude: float
    amount: int
    total_amount: Optional[int]


class AdminProductShow(NamedTuple):
    name: str
    price_name: Optional[str]
    count: int


class UserOrderShow(NamedTuple):
    order_id: OrderId
    amount: int
    total_amount: Optional[int]


class UserProductShow(NamedTuple):
    name: str
    price_name: Optional[str]
    price: int
    count: int
