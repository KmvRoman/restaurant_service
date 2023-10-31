from dataclasses import dataclass
from typing import Optional

from src.domain.product.entities.product import ProductId
from src.domain.user.entities.user import UserId


@dataclass
class DeleteProductFromBasketDtoInput:
    user_id: UserId
    product_id: ProductId
    modification: Optional[int]
