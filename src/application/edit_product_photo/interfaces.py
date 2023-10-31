from src.application.common.interfaces import EditProductPhoto, AddProductPhoto, GetProduct, Committer


class DbGateway(EditProductPhoto, AddProductPhoto, GetProduct, Committer):
    pass
