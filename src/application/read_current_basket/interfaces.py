from src.application.common.interfaces import ReadCurrentBasket, ShippingLength, ReadRestaurantLocationById, Closer


class DbGateway(ReadCurrentBasket, ReadRestaurantLocationById, Closer):
    pass


class ShippingLengthCalculateService(ShippingLength):
    pass
