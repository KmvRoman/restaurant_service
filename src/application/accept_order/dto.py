from dataclasses import dataclass

from src.domain.order.entities.order import OrderId
from src.domain.user.entities.user import UserId


@dataclass
class AcceptOrderDtoInput:
    order_id: OrderId


@dataclass
class AcceptOrderDtoOutput:
    user_id: UserId
