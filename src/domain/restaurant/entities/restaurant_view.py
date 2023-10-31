from dataclasses import dataclass
from typing import NewType

from src.domain.product.entities.product import ProductId
from src.domain.restaurant.constants.constants import MenuProductStatus

RestaurantId = NewType("RestaurantId", int)
CategoryId = NewType("CategoryId", int)
LocationId = NewType("LocationId", int)


@dataclass
class MenuProduct:
    location_id: LocationId
    category_id: CategoryId
    product_id: ProductId
    status: MenuProductStatus


@dataclass
class Category:
    id: CategoryId
    category: str


@dataclass
class RestaurantLocation:
    id: LocationId
    address: str
    latitude: float
    longitude: float


@dataclass
class RestaurantView:
    id: RestaurantId
    name: str
    description: str
    location: list[RestaurantLocation]


@dataclass
class ReadRestaurantBranches:
    location_id: LocationId
    address: str
