from typing import Protocol

from src.domain.order.entities.basket import Basket, ProductBasket
from src.domain.order.entities.basket_view import BasketViewInput
from src.domain.order.entities.order import OrderId, PickUpOrder, ShippingOrder, Order, Location
from src.domain.order.entities.order_view import ReadOrderUser, ReadOrderAdmin, ReadAdminOrderProduct, \
    ReadUserOrderProduct
from src.domain.product.entities.product import Product, ProductId, ProductName, ProductDescription, ProductPrice
from src.domain.product.entities.product_view import ProductView, AdminProductsView, ProductAdmin
from src.domain.restaurant.constants.constants import MenuProductStatus
from src.domain.restaurant.entities.restaurant_view import MenuProduct, RestaurantId, RestaurantLocation, LocationId, \
    CategoryId, RestaurantView, Category, ReadRestaurantBranches
from src.domain.restaurant.entities.stop_list_view import StopList
from src.domain.user.constants.user import Member, Language
from src.domain.user.entities.user import User, UserId


class Committer(Protocol):
    async def commit(self) -> None:
        raise NotImplementedError


class CreateUser(Protocol):
    async def create_user(self, user: User) -> UserId:
        raise NotImplementedError


class EditUserName(Protocol):
    async def edit_user_name(self, name: str, user_id: UserId) -> None:
        raise NotImplementedError


class EditUserPhone(Protocol):
    async def edit_user_phone(self, phone: str, user_id: UserId) -> None:
        raise NotImplementedError


class EditUserLanguage(Protocol):
    async def edit_user_language(self, language: Language, user_id: UserId) -> None:
        raise NotImplementedError


class PromoteUser(Protocol):
    async def promote_user(self, member: Member, user_id: UserId) -> None:
        raise NotImplementedError


class GetUser(Protocol):
    async def get_user_by_user_id(self, user_id: UserId) -> User:
        raise NotImplementedError


class CreateProduct(Protocol):
    async def create_product(self, product: Product) -> ProductId:
        raise NotImplementedError


class CreateMenuProduct(Protocol):
    async def create_menu_product(
            self, locations_id: list[LocationId],
            category_id: CategoryId, product_id: ProductId,
    ) -> None:
        raise NotImplementedError


class GetProduct(Protocol):
    async def get_product_by_product_id(self, product_id: ProductId) -> Product:
        raise NotImplementedError


class GetAdminProduct(Protocol):
    async def get_product_by_menu_product_id(self,  menu_product_id: int) -> ProductAdmin:
        raise NotImplementedError


class EditProductPhoto(Protocol):
    async def edit_product_photo(self, photo: str, product_id: ProductId) -> None:
        raise NotImplementedError


class AddProductPhoto(Protocol):
    async def add_product_photo(self, photo: str, product_id: ProductId) -> None:
        raise NotImplementedError


class EditProductName(Protocol):
    async def edit_product_name(self, name: list[ProductName], product_id: ProductId) -> None:
        raise NotImplementedError


class EditProductDescription(Protocol):
    async def edit_product_description(self, description: list[ProductDescription], product_id: ProductId) -> None:
        raise NotImplementedError


class AddProductDescription(Protocol):
    async def add_product_description(self, description: list[ProductDescription], product_id: ProductId) -> None:
        raise NotImplementedError


class EditProductPrice(Protocol):
    async def edit_product_price(self, price: list[ProductPrice], product_id: ProductId) -> None:
        raise NotImplementedError


class EditProductAvailable(Protocol):
    async def edit_product_available(self, menu_product_id: int, status: MenuProductStatus) -> None:
        raise NotImplementedError


class GetProductLocation(Protocol):
    async def get_product_location(self, menu_product_id: int) -> MenuProduct | None:
        raise NotImplementedError


class DeleteProduct(Protocol):
    async def delete_product(self, product_id: ProductId) -> None:
        raise NotImplementedError


class CreateBasket(Protocol):
    async def create_basket(self, basket: Basket) -> None:
        raise NotImplementedError


class GetBasket(Protocol):
    async def get_basket_by_user_id(self, user_id: UserId) -> Basket:
        raise NotImplementedError


class UpdateProductBasket(Protocol):
    async def update_product_basket(self, product_basket: list[ProductBasket], user_id: UserId) -> None:
        raise NotImplementedError


class CreateShippingOrder(Protocol):
    async def create_shipping_order(self, order: ShippingOrder) -> OrderId:
        raise NotImplementedError


class ExistUserAddress(Protocol):
    async def exist_user_address(self, address: str, user_id: UserId) -> bool:
        raise NotImplementedError


class AddAddressToAddressPool(Protocol):
    async def add_address_to_pool(self, order_id: int) -> None:
        raise NotImplementedError


class CreatePickUpOrder(Protocol):
    async def create_pick_up_order(self, order: PickUpOrder) -> OrderId:
        raise NotImplementedError


class ChoosePaymentMethod(Protocol):
    async def choose_payment_method(self, order: Order) -> None:
        raise NotImplementedError


class ExistOrder(Protocol):
    async def exist_order(self, order_id: OrderId) -> bool:
        raise NotImplementedError


class AcceptOrder(Protocol):
    async def accept_order(self, order_id: OrderId) -> None:
        raise NotImplementedError


class ReadRestaurantsLocations(Protocol):
    async def read_restaurant_locations(self, restaurant_id: RestaurantId) -> list[RestaurantLocation]:
        raise NotImplementedError


class ReadBranches(Protocol):
    async def read_branches(self, restaurant_id: RestaurantId) -> list[ReadRestaurantBranches]:
        raise NotImplementedError


class ReadDetachedBranches(Protocol):
    async def read_detached_branches(self, restaurant_id: RestaurantId) -> list[ReadRestaurantBranches]:
        raise NotImplementedError


class ReadRestaurantLocationById(Protocol):
    async def read_restaurant_location(self, location_id: LocationId) -> Location | None:
        raise NotImplementedError


class ReadStopList(Protocol):
    async def read_stop_list(self, location_id: LocationId, language: Language) -> list[StopList]:
        raise NotImplementedError


class ReadRestaurantLocationsId(Protocol):
    async def read_restaurant_locations_id(self, restaurant_id: RestaurantId) -> list[LocationId]:
        raise NotImplementedError


class ReadRestaurantData(Protocol):
    async def read_restaurant_data(
            self, restaurant_id: RestaurantId, language: Language,
    ) -> RestaurantView:
        raise NotImplementedError


class ReadProducts(Protocol):
    async def read_products(self, location_id: LocationId, language: Language) -> list[ProductView]:
        raise NotImplementedError


class ReadCategoryProducts(Protocol):
    async def read_category_products(
            self, location_id: LocationId, language: Language, category_id: CategoryId,
    ) -> list[AdminProductsView]:
        raise NotImplementedError


class ReadOrderForUser(Protocol):
    async def read_order_user(self, order_id: OrderId, language: Language) -> ReadOrderUser:
        raise NotImplementedError


class ReadOrderProductForUser(Protocol):
    async def read_user_order_product(self, order_id: OrderId, language: Language) -> list[ReadUserOrderProduct]:
        raise NotImplementedError


class ReadOrderForAdmin(Protocol):
    async def read_order_admin(self, order_id: OrderId) -> ReadOrderAdmin:
        raise NotImplementedError


class ReadOrderProductForAdmin(Protocol):
    async def read_admin_order_product(self, order_id: OrderId, language: Language) -> list[ReadAdminOrderProduct]:
        raise NotImplementedError


class ReadCategories(Protocol):
    async def read_categories(self, restaurant_id: RestaurantId, language: Language) -> list[Category]:
        raise NotImplementedError


class ReadCurrentBasket(Protocol):
    async def read_current_basket(self, user_id: UserId, language: Language) -> BasketViewInput:
        raise NotImplementedError


class ReadRestaurantLocation(Protocol):
    async def read_restaurant_location(self, location_id: LocationId) -> RestaurantLocation:
        raise NotImplementedError


class ReadUserAddresses(Protocol):
    async def read_user_addresses(self, user_id: UserId) -> list[str]:
        raise NotImplementedError


class ReadRestaurantAddresses(Protocol):
    async def read_restaurant_addresses(self, restaurant_id: RestaurantId) -> list[str]:
        raise NotImplementedError


class ReadRestaurantLocationIdByAddress(Protocol):
    async def read_restaurant_location_id_by_address(self, restaurant_id: RestaurantId, address: str) -> int:
        raise NotImplementedError


class ReadUserLocationByAddress(Protocol):
    async def read_user_location_by_address(self, address: str, user_id: UserId) -> Location:
        raise NotImplementedError


class ShippingLength(Protocol):
    async def get_shipping_length(self, user_location: Location, restaurant_location: Location) -> float:
        raise NotImplementedError


class GetAddressFromLocation(Protocol):
    async def get_address(self, user_location: Location) -> str:
        raise NotImplementedError


class ReadBranchGroup(Protocol):
    async def read_branch_group(self, restaurant_location_id: int) -> int:
        raise NotImplementedError
