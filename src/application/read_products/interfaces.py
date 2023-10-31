from src.application.common.interfaces import ReadProducts, ReadRestaurantsLocations


class DbGateway(ReadProducts, ReadRestaurantsLocations):
    pass
