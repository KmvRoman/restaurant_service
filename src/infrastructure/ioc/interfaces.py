from typing import Protocol

from src.application.accept_order.use_case import AcceptOrderCase
from src.application.add_product_to_basket.use_case import AddProductToBasketCase
from src.application.choose_payment_method.use_case import ChoosePaymentMethodCase
from src.application.create_order.use_case import CreateOrderCase
from src.application.create_product.use_case import CreateProductCase
from src.application.create_user.use_case import CreateUserUseCase
from src.application.delete_product_from_basket.use_case import DeleteProductFromBasketCase
from src.application.delete_product_from_system.use_case import DeleteProductCase
from src.application.edit_product_available.use_case import EditProductAvailableCase
from src.application.edit_product_description.use_case import EditProductDescriptionCase
from src.application.edit_product_name.use_case import EditProductNameCase
from src.application.edit_product_photo.use_case import EditProductPhotoCase
from src.application.edit_product_price.use_case import EditProductPriceCase
from src.application.edit_user_language.use_case import UpdateUserLanguageCase
from src.application.edit_user_name.use_case import EditUserNameCase
from src.application.edit_user_phone.use_case import UpdateUserPhoneCase
from src.application.get_address_from_location.use_case import GetLocationFromAddressCase
from src.application.promote_user.use_case import PromoteUserCase
from src.application.read_branches.use_case import ReadRestaurantBranchesCase
from src.application.read_categories.use_case import ReadCategoriesCase
from src.application.read_category_products.use_case import ReadCategoryProductsCase
from src.application.read_current_basket.use_case import ReadCurrentBasketCase
from src.application.read_nearest_location_id.use_case import ReadNearestRestaurantLocation
from src.application.read_order_admin.use_case import ReadOrderAdminCase
from src.application.read_order_user.use_case import ReadOrderUserCase
from src.application.read_product_admin.use_case import ReadProductAdminCase
from src.application.read_products.use_case import ReadProductsCase
from src.application.read_restaurant_addresses.use_case import ReadRestaurantAddressesCase
from src.application.read_restaurant_data.use_case import ReadRestaurantDataCase
from src.application.read_restaurant_location.use_case import ReadRestaurantLocationCase
from src.application.read_restaurant_location_id_by_address.use_case import ReadRestaurantLocationIdByAddressCase
from src.application.read_restaurants.use_case import ReadRestaurantsLocationsCase
from src.application.read_stop_list.use_case import ReadStopListCase
from src.application.read_user_addresses.use_case import ReadUserAddressesCase
from src.application.read_user_location_by_address.use_case import ReadUserLocationByAddressCase
from src.application.read_user_profile.use_case import ReadUserProfileCase


class InteractorFactory(Protocol):
    async def commit(self): ...

    async def create_user(self) -> CreateUserUseCase: ...

    async def edit_user_name(self) -> EditUserNameCase: ...

    async def edit_user_phone(self) -> UpdateUserPhoneCase: ...

    async def edit_user_language(self) -> UpdateUserLanguageCase: ...

    async def promote_user(self) -> PromoteUserCase: ...

    async def accept_order(self) -> AcceptOrderCase: ...

    async def add_product_to_basket(self) -> AddProductToBasketCase: ...

    async def choose_payment_method(self) -> ChoosePaymentMethodCase: ...

    async def create_order(self) -> CreateOrderCase: ...

    async def create_product(self) -> CreateProductCase: ...

    async def delete_product_from_basket(self) -> DeleteProductFromBasketCase: ...

    async def delete_product_from_system(self) -> DeleteProductCase: ...

    async def edit_product_available(self) -> EditProductAvailableCase: ...

    async def edit_product_description(self) -> EditProductDescriptionCase: ...

    async def edit_product_name(self) -> EditProductNameCase: ...

    async def edit_product_photo(self) -> EditProductPhotoCase: ...

    async def edit_product_price(self) -> EditProductPriceCase: ...

    async def read_current_basket(self) -> ReadCurrentBasketCase: ...

    async def read_order_admin(self) -> ReadOrderAdminCase: ...

    async def read_order_user(self) -> ReadOrderUserCase: ...

    async def read_products(self) -> ReadProductsCase: ...

    async def read_restaurant_data(self) -> ReadRestaurantDataCase: ...

    async def read_restaurants(self) -> ReadRestaurantsLocationsCase: ...

    async def read_restaurant_location(self) -> ReadRestaurantLocationCase: ...

    async def read_stop_list(self) -> ReadStopListCase: ...

    async def read_user_profile(self) -> ReadUserProfileCase: ...

    async def read_categories(self) -> ReadCategoriesCase: ...

    async def read_category_products(self) -> ReadCategoryProductsCase: ...

    async def read_branches(self) -> ReadRestaurantBranchesCase: ...

    async def read_product_admin(self) -> ReadProductAdminCase: ...

    async def read_user_addresses(self) -> ReadUserAddressesCase: ...

    async def read_restaurant_addresses(self) -> ReadRestaurantAddressesCase: ...

    async def get_address_from_location(self) -> GetLocationFromAddressCase: ...

    async def read_restaurant_location_id_by_address(self) -> ReadRestaurantLocationIdByAddressCase: ...

    async def read_user_location_by_address(self) -> ReadUserLocationByAddressCase: ...

    async def read_nearest_restaurant_location_id(self) -> ReadNearestRestaurantLocation: ...