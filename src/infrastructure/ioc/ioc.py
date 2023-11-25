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
from src.application.read_group_branch.use_case import ReadBranchGroupCase
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
from src.domain.order.services.basket import BasketService
from src.domain.order.services.basket_view import BasketViewService
from src.domain.order.services.order import OrderService
from src.domain.product.services.product import ProductService
from src.domain.restaurant.services.restaurant_location import RestaurantService
from src.domain.user.services.user import UserService
from src.infrastructure.cache.redis_cache import RedisCacheSystem
from src.infrastructure.config.config import Config
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.infrastructure.ioc.interfaces import InteractorFactory
from src.infrastructure.web.get_address_from_location.get_address import GetAddressFromLocation
from src.infrastructure.web.shipping_length_calculate.shipping_length import ShippingLengthImpl


class IoC(InteractorFactory):
    def __init__(self, db_gateway: UserRepository, redis_cache: RedisCacheSystem, config: Config):
        self.db_gateway = db_gateway
        self.user_service = UserService()
        self.order_service = OrderService()
        self.product_service = ProductService()
        self.restaurant_service = RestaurantService()
        self.basket_service = BasketService()
        self.basket_view_service = BasketViewService()
        self.shipping_length_resource = ShippingLengthImpl(redis_cache=redis_cache)
        self.address_service = GetAddressFromLocation(
            apikey=config.geocode.api_key, format=config.geocode.format, lang=config.geocode.lang,
        )

    async def create_user(self) -> CreateUserUseCase:
        return CreateUserUseCase(db_gateway=self.db_gateway, user_service=self.user_service)

    async def edit_user_name(self) -> EditUserNameCase:
        return EditUserNameCase(db_gateway=self.db_gateway, user_service=self.user_service)

    async def edit_user_phone(self) -> UpdateUserPhoneCase:
        return UpdateUserPhoneCase(db_gateway=self.db_gateway, user_service=self.user_service)

    async def edit_user_language(self) -> UpdateUserLanguageCase:
        return UpdateUserLanguageCase(db_gateway=self.db_gateway, user_service=self.user_service)

    async def promote_user(self) -> PromoteUserCase:
        return PromoteUserCase(db_gateway=self.db_gateway, user_service=self.user_service)

    async def accept_order(self) -> AcceptOrderCase:
        return AcceptOrderCase(db_gateway=self.db_gateway, order_service=self.order_service)

    async def add_product_to_basket(self) -> AddProductToBasketCase:
        return AddProductToBasketCase(db_gateway=self.db_gateway, basket_service=self.basket_service)

    async def choose_payment_method(self) -> ChoosePaymentMethodCase:
        return ChoosePaymentMethodCase(db_gateway=self.db_gateway, order_service=self.order_service)

    async def create_order(self) -> CreateOrderCase:
        return CreateOrderCase(
            db_gateway=self.db_gateway, order_service=self.order_service,
        )

    async def create_product(self) -> CreateProductCase:
        return CreateProductCase(db_gateway=self.db_gateway, product_service=self.product_service)

    async def delete_product_from_basket(self) -> DeleteProductFromBasketCase:
        return DeleteProductFromBasketCase(db_gateway=self.db_gateway, basket_service=self.basket_service)

    async def delete_product_from_system(self) -> DeleteProductCase:
        return DeleteProductCase(db_gateway=self.db_gateway, product_service=self.product_service)

    async def edit_product_available(self) -> EditProductAvailableCase:
        return EditProductAvailableCase(db_gateway=self.db_gateway, restaurant_service=self.restaurant_service)

    async def edit_product_description(self) -> EditProductDescriptionCase:
        return EditProductDescriptionCase(db_gateway=self.db_gateway, product_service=self.product_service)

    async def edit_product_name(self) -> EditProductNameCase:
        return EditProductNameCase(db_gateway=self.db_gateway, product_service=self.product_service)

    async def edit_product_photo(self) -> EditProductPhotoCase:
        return EditProductPhotoCase(db_gateway=self.db_gateway, product_service=self.product_service)

    async def edit_product_price(self) -> EditProductPriceCase:
        return EditProductPriceCase(db_gateway=self.db_gateway, product_service=self.product_service)

    async def read_current_basket(self) -> ReadCurrentBasketCase:
        return ReadCurrentBasketCase(
            db_gateway=self.db_gateway,
            basket_view_service=self.basket_view_service,
            shipping_length=self.shipping_length_resource,
            order_service=self.order_service,
        )

    async def read_order_admin(self) -> ReadOrderAdminCase:
        return ReadOrderAdminCase(db_gateway=self.db_gateway)

    async def read_order_user(self) -> ReadOrderUserCase:
        return ReadOrderUserCase(db_gateway=self.db_gateway)

    async def read_products(self) -> ReadProductsCase:
        return ReadProductsCase(db_gateway=self.db_gateway, restaurant_service=self.restaurant_service)

    async def read_restaurant_data(self) -> ReadRestaurantDataCase:
        return ReadRestaurantDataCase(db_gateway=self.db_gateway)

    async def read_restaurants(self) -> ReadRestaurantsLocationsCase:
        return ReadRestaurantsLocationsCase(db_gateway=self.db_gateway)

    async def read_restaurant_location(self) -> ReadRestaurantLocationCase:
        return ReadRestaurantLocationCase(db_gateway=self.db_gateway)

    async def read_stop_list(self) -> ReadStopListCase:
        return ReadStopListCase(db_gateway=self.db_gateway)

    async def read_user_profile(self) -> ReadUserProfileCase:
        return ReadUserProfileCase(db_gateway=self.db_gateway)

    async def read_categories(self) -> ReadCategoriesCase:
        return ReadCategoriesCase(db_gateway=self.db_gateway)

    async def read_category_products(self) -> ReadCategoryProductsCase:
        return ReadCategoryProductsCase(db_gateway=self.db_gateway)

    async def read_branches(self) -> ReadRestaurantBranchesCase:
        return ReadRestaurantBranchesCase(db_gateway=self.db_gateway)

    async def read_product_admin(self) -> ReadProductAdminCase:
        return ReadProductAdminCase(db_gateway=self.db_gateway)

    async def read_user_addresses(self) -> ReadUserAddressesCase:
        return ReadUserAddressesCase(db_gateway=self.db_gateway)

    async def read_restaurant_addresses(self) -> ReadRestaurantAddressesCase:
        return ReadRestaurantAddressesCase(db_gateway=self.db_gateway)

    async def get_address_from_location(self) -> GetLocationFromAddressCase:
        return GetLocationFromAddressCase(address_service=self.address_service)

    async def read_restaurant_location_id_by_address(self) -> ReadRestaurantLocationIdByAddressCase:
        return ReadRestaurantLocationIdByAddressCase(db_gateway=self.db_gateway)

    async def read_user_location_by_address(self) -> ReadUserLocationByAddressCase:
        return ReadUserLocationByAddressCase(db_gateway=self.db_gateway)

    async def read_nearest_restaurant_location_id(self) -> ReadNearestRestaurantLocation:
        return ReadNearestRestaurantLocation(db_gateway=self.db_gateway, restaurant_service=self.restaurant_service)

    async def read_branch_group(self) -> ReadBranchGroupCase:
        return ReadBranchGroupCase(db_gateway=self.db_gateway)
