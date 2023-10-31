from enum import Enum


class ProductMode(str, Enum):
    default = "default"
    extend = "extend"


class ProductStatus(str, Enum):
    active = "active"
    deleted = "deleted"
