from src.application.common.interfaces import EditProductName, GetProduct, Committer


class DbGateway(EditProductName, GetProduct, Committer):
    pass
