from dataclasses import dataclass
from typing import Optional

from src.domain.order.constants.order import OrderType, PaymentType
from src.domain.order.entities.order import OrderId, Location


@dataclass
class ReadUserOrderProduct:
    name: str
    price: int
    count: int
    total_price: int


@dataclass
class ReadAdminOrderProduct:
    name: str
    count: int


@dataclass
class ReadOrderUser:
    order_type: OrderType
    phone: str
    address: Optional[str]
    comment: Optional[str]
    products: list[ReadUserOrderProduct]
    amount: Optional[int]
    shipping_amount: Optional[int]
    shipping_length: Optional[float]
    total_cost: int


@dataclass
class ReadOrderAdmin:
    order_id: OrderId
    order_type: OrderType
    products: list[ReadAdminOrderProduct]
    name: str
    phone: str
    payment_type: PaymentType
    address: Optional[str]
    comment: Optional[str]
    location: Optional[Location]
    shipping_amount: Optional[str]
    total_cost: int
