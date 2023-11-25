class ApplicationError(Exception):
    pass


class UserNotExistError(ApplicationError):
    pass


class ProductNotExistError(ApplicationError):
    pass


class RestaurantsNotFound(ApplicationError):
    pass


class RestaurantDataNotFound(ApplicationError):
    pass


class RestaurantLocationIdNotFound(ApplicationError):
    pass


class UserOrderNotFound(ApplicationError):
    pass


class AdminOrderNotFound(ApplicationError):
    pass


class CurrentBasketNotFound(ApplicationError):
    pass


class ProductsIsEmpty(ApplicationError):
    pass


class ProductNotFound(ApplicationError):
    pass


class RestaurantLocationNotFound(ApplicationError):
    pass


class RestaurantLocationsNotFound(ApplicationError):
    pass


class OrderNotFound(ApplicationError):
    pass


class CategoryProductsIsEmpty(ApplicationError):
    pass


class EmptyStopList(ApplicationError):
    pass


class UserLocationNotFound(ApplicationError):
    pass


class GroupIdCantBeNone(ApplicationError):
    pass
