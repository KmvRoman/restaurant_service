from dataclasses import dataclass
from typing import Optional

from src.domain.order.constants.order import OrderType, PaymentType
from src.domain.order.entities.order import OrderId, Location


@dataclass
class ReadUserOrderProduct:
    name: str
    price_name: Optional[str]
    price: int
    count: int
    total_price: int


@dataclass
class ReadAdminOrderProduct:
    name: str
    price_name: Optional[str]
    count: int


@dataclass
class ReadOrderUser:
    order_id: OrderId
    products: list[ReadUserOrderProduct]
    amount: Optional[int]
    total_cost: int


@dataclass
class ReadOrderAdmin:
    order_id: OrderId
    products: list[ReadAdminOrderProduct]
    name: str
    phone: str
    payment_type: PaymentType
    address: Optional[str]
    comment: Optional[str]
    location: Optional[Location]
    shipping_amount: Optional[int]
    total_cost: int
