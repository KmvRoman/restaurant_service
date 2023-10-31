from src.application.common.interfaces import EditProductDescription, AddProductDescription, GetProduct, Committer


class DbGateway(EditProductDescription, AddProductDescription, GetProduct, Committer):
    pass
