from src.application.common.interfaces import (
    CreateShippingOrder, CreatePickUpOrder,
    Committer, ShippingLength, ReadRestaurantLocationById, AddAddressToAddressPool, ExistUserAddress,
)


class DbGateway(
    CreateShippingOrder, CreatePickUpOrder, ReadRestaurantLocationById,
    ExistUserAddress, AddAddressToAddressPool, Committer
):
    pass


class ShippingLengthResource(ShippingLength):
    pass
