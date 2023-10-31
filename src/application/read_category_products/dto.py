from dataclasses import dataclass

from src.domain.product.constants.product import ProductStatus
from src.domain.product.entities.product import ProductId
from src.domain.restaurant.constants.constants import MenuProductStatus
from src.domain.restaurant.entities.restaurant_view import RestaurantId, LocationId, CategoryId
from src.domain.user.constants.user import Language


@dataclass
class ReadCategoryProductsDtoInput:
    location_id: LocationId
    category_id: CategoryId
    language: Language


@dataclass
class CategoryProduct:
    menu_product_id: int
    name: str
    menu_product_status: MenuProductStatus


@dataclass
class ReadCategoryDtoOutput:
    category_name: str
    products: list[CategoryProduct]
