from src.application.common.interfaces import ReadCurrentBasket, ShippingLength, ReadRestaurantLocationById


class DbGateway(ReadCurrentBasket, ReadRestaurantLocationById):
    pass


class ShippingLengthCalculateService(ShippingLength):
    pass
