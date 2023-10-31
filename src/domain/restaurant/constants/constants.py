from enum import Enum


class MenuProductStatus(str, Enum):
    available = "available"
    not_available = "not_available"
