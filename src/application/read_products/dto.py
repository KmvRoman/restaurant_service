from dataclasses import dataclass
from typing import Optional

from src.domain.order.entities.order import Location
from src.domain.product.constants.product import ProductMode, ProductStatus
from src.domain.product.entities.product import ProductId
from src.domain.product.entities.product_view import Price, ProductsCategory
from src.domain.restaurant.constants.constants import MenuProductStatus
from src.domain.restaurant.entities.restaurant_view import RestaurantId
from src.domain.user.constants.user import Language


@dataclass
class ReadProductsDtoInput:
    restaurant_id: RestaurantId
    user_location: Location
    language: Language


@dataclass
class ReadProductsDtoOutput:
    id: int
    category: str
    products: list[ProductsCategory]
