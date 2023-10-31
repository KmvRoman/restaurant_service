from src.application.common.interfaces import EditProductAvailable, Committer, GetProductLocation


class DbGateway(EditProductAvailable, GetProductLocation, Committer):
    pass
