from src.application.common.interfaces import CreateProduct, Committer, CreateMenuProduct, ReadRestaurantLocationsId


class DbGateway(CreateProduct, CreateMenuProduct, ReadRestaurantLocationsId, Committer):
    pass
