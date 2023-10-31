from src.application.common.interfaces import EditProductPrice, GetProduct, Committer


class DbGateway(EditProductPrice, GetProduct, Committer):
    pass
