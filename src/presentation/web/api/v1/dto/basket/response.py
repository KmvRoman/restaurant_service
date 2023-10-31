from typing import Optional

from pydantic import BaseModel

from src.domain.order.constants.order import OrderType
from src.domain.product.constants.product import ProductMode, ProductStatus
from src.domain.product.entities.product import ProductId
from src.domain.restaurant.constants.constants import MenuProductStatus
from src.domain.user.entities.user import UserId


class ProductPrice(BaseModel):
    id: int
    name: Optional[str]
    price: int


class ProductsPerCategory(BaseModel):
    menu_product_id: int
    product_id: ProductId
    photo: Optional[str]
    name: str
    description: Optional[str]
    mode: ProductMode
    price: list[ProductPrice]
    product_status: ProductStatus
    menu_product_status: MenuProductStatus


class CategoryProducts(BaseModel):
    id: int
    category: str
    products: list[ProductsPerCategory]


class SuccessResponse(BaseModel):
    ok: bool = True


class PreparedProducts(BaseModel):
    product_id: ProductId
    photo: Optional[str]
    name: str
    modification: Optional[int]
    price_name: Optional[str]
    count: int
    price: int
    amount: int


class GetBasketResponse(BaseModel):
    user_id: UserId
    products: list[PreparedProducts]
    order_type: OrderType
    shipping_amount: Optional[int]
    amount: int
    total_amount: int


class GetBannersResponse(BaseModel):
    banners: list[str]
