from typing import NamedTuple, Optional

from src.domain.order.constants.basket import BasketStatus
from src.domain.product.constants.product import ProductMode, ProductStatus
from src.domain.product.entities.product import ProductId
from src.domain.restaurant.constants.constants import MenuProductStatus
from src.domain.restaurant.entities.restaurant_view import CategoryId
from src.domain.user.constants.user import Language
from src.domain.user.entities.user import UserId


class ShowProduct(NamedTuple):
    category_id: CategoryId
    category_name: str
    menu_product_id: int
    product_id: ProductId
    photo: Optional[str]
    name: str
    description: Optional[str]
    mode: ProductMode
    price_id: int
    price: int
    price_name: Optional[str]
    product_status: ProductStatus
    menu_product_status: MenuProductStatus


class ShowBasket(NamedTuple):
    user_id: UserId
    product_id: ProductId
    count: int
    modification: Optional[int]
    status: BasketStatus


class ViewBasket(NamedTuple):
    user_id: UserId
    product_id: ProductId
    photo: Optional[str]
    name: str
    modification: Optional[int]
    price_name: Optional[str]
    count: int
    price: int


class ShowProductsAdminMenu(NamedTuple):
    category_name: str
    menu_product_id: int
    name: str
    menu_product_status: MenuProductStatus


class ShowFullProduct(NamedTuple):
    id: int
    photo: Optional[str]
    name: str
    name_language: Language
    description: Optional[str]
    description_language: Optional[Language]
    mode: ProductMode
    price_id: int
    price: int
    price_name: Optional[str]
    price_name_language: Optional[Language]
    product_status: ProductStatus
    menu_product_status: MenuProductStatus


class ShowCoreProduct(NamedTuple):
    id: ProductId
    photo: Optional[str]
    name: str
    name_language: Language
    description: Optional[str]
    description_language: Optional[Language]
    mode: ProductMode
    price_id: int
    price: int
    price_name: Optional[str]
    price_name_language: Optional[Language]
    product_status: ProductStatus
