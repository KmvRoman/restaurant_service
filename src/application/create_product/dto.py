from dataclasses import dataclass
from typing import Optional

from src.domain.product.constants.product import ProductMode
from src.domain.product.entities.product import ProductName, ProductDescription, ProductPrice, ProductId
from src.domain.restaurant.entities.restaurant_view import CategoryId, RestaurantId


@dataclass
class CreateProductDtoInput:
    restaurant_id: RestaurantId
    category_id: CategoryId
    photo: Optional[str]
    name: list[ProductName]
    description: Optional[list[ProductDescription]]
    mode: ProductMode
    price: list[ProductPrice]


@dataclass
class CreateProductDtoOutput:
    product_id: ProductId
