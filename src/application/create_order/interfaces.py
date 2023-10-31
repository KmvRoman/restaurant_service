from src.application.common.interfaces import (
    CreateShippingOrder, CreatePickUpOrder,
    Committer, ShippingLength, ReadRestaurantLocationById,
)


class DbGateway(CreateShippingOrder, CreatePickUpOrder, ReadRestaurantLocationById, Committer):
    pass


class ShippingLengthResource(ShippingLength):
    pass
