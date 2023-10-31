from src.application.common.interfaces import UpdateProductBasket, GetBasket, Committer, CreateBasket


class DbGateway(CreateBasket, UpdateProductBasket, GetBasket, Committer):
    pass
