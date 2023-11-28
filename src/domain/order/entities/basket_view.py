from dataclasses import dataclass
from typing import Optional

from src.domain.order.constants.order import OrderType
from src.domain.order.entities.order import OrderId
from src.domain.product.entities.product import ProductId
from src.domain.user.entities.user import UserId


@dataclass
class PreparedProductInput:
    product_id: ProductId
    photo: str
    modification: Optional[int]
    product_name: str
    price_name: Optional[str]
    count: int
    price: int


@dataclass
class PreparedProductOutput:
    product_id: ProductId
    photo: str
    name: str
    modification: Optional[int]
    price_name: Optional[str]
    count: int
    price: int
    amount: int


@dataclass
class BasketViewInput:
    user_id: UserId
    prepared: list[PreparedProductInput]


@dataclass
class BasketViewOutput:
    user_id: UserId
    prepared: list[PreparedProductOutput]
    order_type: OrderType
    shipping_amount: Optional[int]
    amount: int
    total_amount: int
