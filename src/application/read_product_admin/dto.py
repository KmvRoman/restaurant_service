from dataclasses import dataclass
from typing import Optional

from src.domain.product.constants.product import ProductMode, ProductStatus
from src.domain.product.entities.product import Product, ProductId, ProductName, ProductDescription
from src.domain.product.entities.product_view import AdminProductPrice
from src.domain.restaurant.constants.constants import MenuProductStatus


@dataclass
class ReadProductDtoInput:
    menu_product_id: int


@dataclass
class ReadProductDtoOutput:
    id: Optional[ProductId]
    photo: Optional[str]
    name: list[ProductName]
    description: Optional[list[ProductDescription]]
    mode: ProductMode
    price: list[AdminProductPrice]
    product_status: ProductStatus
    menu_product_status: MenuProductStatus
