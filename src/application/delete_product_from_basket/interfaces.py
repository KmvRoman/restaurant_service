from src.application.common.interfaces import UpdateProductBasket, GetBasket, Committer


class DbGateway(UpdateProductBasket, GetBasket, Committer):
    pass
