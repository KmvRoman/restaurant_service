class DatabaseException(Exception):
    pass


class ModificationSelectedError(DatabaseException):
    def __init__(self):
        self.message = "Selected mode not found in product"


class ProductNotFound(DatabaseException):
    def __init__(self, product_id: int):
        self.message = f"Product with id - {product_id} not found"


class UserNotFoundDbError(DatabaseException):
    def __init__(self, user_id: int):
        self.message = f"User with id - {user_id} not found"
