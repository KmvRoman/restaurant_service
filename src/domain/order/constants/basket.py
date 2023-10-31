from enum import Enum


class BasketStatus(str, Enum):
    prepare = "prepare"
    complete = "complete"
    reject = "reject"
