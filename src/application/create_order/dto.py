from dataclasses import dataclass
from typing import Optional

from src.domain.order.constants.order import OrderType
from src.domain.order.entities.order import ProductOrder, Location, OrderId
from src.domain.restaurant.entities.restaurant_view import LocationId
from src.domain.user.entities.user import UserId


@dataclass
class CreateOrderDtoInput:
    restaurant_location_id: LocationId
    user_id: UserId
    phone: str
    order_type: OrderType
    products: list[ProductOrder]
    location: Optional[Location]
    address: Optional[str]
    comment: Optional[str]
    shipping_length: Optional[float]


@dataclass
class CreateOrderDtoOutput:
    order_id: OrderId
