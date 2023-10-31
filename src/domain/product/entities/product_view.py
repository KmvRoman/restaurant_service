from dataclasses import dataclass
from typing import Optional

from src.domain.product.constants.product import ProductMode, ProductStatus
from src.domain.product.entities.product import ProductId, ProductName, ProductDescription, ProductPriceName
from src.domain.restaurant.constants.constants import MenuProductStatus


@dataclass
class Price:
    id: int
    name: Optional[str]
    price: int


@dataclass
class ProductsCategory:
    menu_product_id: int
    product_id: ProductId
    photo: str
    name: str
    description: str
    mode: ProductMode
    price: list[Price]
    product_status: ProductStatus
    menu_product_status: MenuProductStatus


@dataclass
class ProductView:
    id: int
    category: str
    products: list[ProductsCategory]


@dataclass
class AdminProductsView:
    category_name: str
    menu_product_id: int
    name: str
    menu_product_status: MenuProductStatus


@dataclass
class AdminProductPrice:
    id: int
    name: Optional[list[ProductPriceName]]
    price: int


@dataclass
class ProductAdmin:
    id: Optional[ProductId]
    photo: Optional[str]
    name: list[ProductName]
    description: Optional[list[ProductDescription]]
    mode: ProductMode
    price: list[AdminProductPrice]
    product_status: ProductStatus
    menu_product_status: MenuProductStatus
