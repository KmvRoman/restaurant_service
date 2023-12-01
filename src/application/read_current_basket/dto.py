from dataclasses import dataclass
from typing import Optional

from src.domain.order.constants.order import OrderType
from src.domain.order.entities.order import Location
from src.domain.product.entities.product import ProductId
from src.domain.restaurant.entities.restaurant_view import RestaurantId, LocationId
from src.domain.user.constants.user import Language
from src.domain.user.entities.user import UserId


@dataclass
class ReadCurrentBasketDtoInput:
    user_id: UserId
    user_location: Location
    restaurant_location_id: LocationId
    order_type: OrderType
    language: Language


@dataclass
class PreparedBasketProduct:
    product_id: ProductId
    photo: Optional[str]
    name: str
    count: int
    price: int
    modification: Optional[int]
    price_name: Optional[str]
    amount: int


@dataclass
class ReadCurrentBasketDtoOutput:
    user_id: UserId
    prepared: list[PreparedBasketProduct]
    order_type: OrderType
    shipping_amount: Optional[int]
    shipping_length: Optional[float]
    amount: int
    total_amount: int
