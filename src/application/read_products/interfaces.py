from src.application.common.interfaces import ReadProducts, ReadRestaurantsLocations, Closer


class DbGateway(ReadProducts, ReadRestaurantsLocations, Closer):
    pass
