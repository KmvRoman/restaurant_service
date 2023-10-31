from src.domain.common.exceptions.exceptions import DomainError


class ProductNameError(DomainError):
    pass


class ProductNameNotFoundError(DomainError):
    pass


class ProductDescriptionError(DomainError):
    pass


class ProductDescriptionNotFound(DomainError):
    pass


class ProductPriceNameError(DomainError):
    pass


class ProductPriceNameNotExist(DomainError):
    pass


class ProductModeError(DomainError):
    pass


class ProductModeNotFound(DomainError):
    pass


class ProductPriceNotFoundError(DomainError):
    pass
