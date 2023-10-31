from dataclasses import dataclass
from typing import NewType, Optional

from src.domain.product.constants.product import ProductMode, ProductStatus
from src.domain.user.constants.user import Language

ProductId = NewType("ProductId", int)


@dataclass
class ProductName:
    name: str
    language: Language


@dataclass
class ProductDescription:
    description: str
    language: Language


@dataclass
class ProductPriceName:
    name: str
    language: Language


@dataclass
class ProductPrice:
    name: Optional[list[ProductPriceName]]
    price: int


@dataclass
class Product:
    id: Optional[ProductId]
    photo: Optional[str]
    name: list[ProductName]
    description: Optional[list[ProductDescription]]
    mode: ProductMode
    price: list[ProductPrice]
    status: ProductStatus
