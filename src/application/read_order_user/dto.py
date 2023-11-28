from dataclasses import dataclass
from typing import Optional

from src.domain.order.constants.order import OrderType
from src.domain.order.entities.order import OrderId
from src.domain.order.entities.order_view import ReadUserOrderProduct
from src.domain.user.constants.user import Language


@dataclass
class ReadUserOrderDtoInput:
    order_id: OrderId
    language: Language


@dataclass
class ReadUserOrderDtoOutput:
    order_id: OrderId
    products: list[ReadUserOrderProduct]
    amount: Optional[int]
    total_cost: int
