from typing import Optional

from pydantic import BaseModel

from src.domain.order.constants.order import OrderType
from src.domain.product.entities.product import ProductId
from src.domain.restaurant.entities.restaurant_view import RestaurantId, LocationId
from src.domain.user.constants.user import Language
from src.domain.user.entities.user import UserId


class Location(BaseModel):
    latitude: float
    longitude: float


class GetProductsRequest(BaseModel):
    restaurant_id: RestaurantId
    user_location: Location
    language: Language


class AddProductRequest(BaseModel):
    user_id: UserId
    product_id: ProductId
    count: int
    modification: Optional[int] = None


class DeleteProductRequest(BaseModel):
    user_id: UserId
    product_id: ProductId
    modification: Optional[int] = None


class GetBasketRequest(BaseModel):
    user_id: UserId
    user_location: Optional[Location] = None
    restaurant_location_id: LocationId
    order_type: OrderType
    language: Language
