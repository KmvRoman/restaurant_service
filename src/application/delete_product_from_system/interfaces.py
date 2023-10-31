from src.application.common.interfaces import DeleteProduct, GetProduct, Committer


class DbGateway(DeleteProduct, GetProduct, Committer):
    pass
