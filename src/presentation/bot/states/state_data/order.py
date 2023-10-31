from typing import Optional

from pydantic import BaseModel

from src.application.read_current_basket.dto import PreparedBasketProduct
from src.domain.order.constants.order import OrderType, PaymentType, OrderStatus
from src.domain.order.entities.order import OrderId, ProductOrder, Location
from src.domain.restaurant.entities.restaurant_view import LocationId
from src.domain.user.entities.user import UserId


class ShippingData(BaseModel):
    order_id: OrderId | None = None
    user_id: UserId | None = None
    phone: str | None = None
    payment_type: Optional[PaymentType] | None = None
    order_type: OrderType = OrderType.shipping
    status: OrderStatus | None = None
    location: Location | None = None
    address: str | None = None
    comment: str | None = None
    amount: int | None = None
    shipping_length: float | None = None
    total_amount: int | None = None
    products: list[PreparedBasketProduct] = []


class PickupData(BaseModel):
    order_id: OrderId | None = None
    user_id: UserId | None = None
    phone: str | None = None
    payment_type: Optional[PaymentType] | None = None
    order_type: OrderType = OrderType.pickup
    status: OrderStatus | None = None
    restaurant_location_id: LocationId | None = None
    total_amount: int | None = None
    products: list[PreparedBasketProduct] = []
