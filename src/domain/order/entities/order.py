from dataclasses import dataclass
from typing import Optional, NewType

from src.domain.order.constants.order import PaymentType, OrderType, OrderStatus
from src.domain.product.entities.product import ProductId
from src.domain.user.entities.user import UserId

OrderId = NewType("OrderId", int)


@dataclass
class ProductOrder:
    product_id: ProductId
    modification: Optional[str]
    count: int
    price: int


@dataclass
class Order:
    id: Optional[OrderId]
    user_id: UserId
    phone: str
    payment_type: Optional[PaymentType]
    order_type: OrderType
    products: list[ProductOrder]
    amount: int
    status: OrderStatus
    total_amount: int


@dataclass
class Location:
    latitude: float
    longitude: float


@dataclass
class ShippingOrder(Order):
    location: Location
    address: str
    comment: str
    shipping_length: float


@dataclass
class PickUpOrder(Order):
    pass
