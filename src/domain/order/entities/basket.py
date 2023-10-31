from dataclasses import dataclass
from typing import Optional

from src.domain.order.constants.basket import BasketStatus
from src.domain.product.entities.product import ProductId
from src.domain.user.entities.user import UserId


@dataclass
class ProductBasket:
    product_id: ProductId
    count: int
    modification: Optional[int]


@dataclass
class Basket:
    user_id: UserId
    prepared: list[ProductBasket]
    status: BasketStatus
