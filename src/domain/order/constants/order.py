from enum import Enum


class PaymentType(str, Enum):
    cache = "cache"
    card = "card"


class OrderType(str, Enum):
    shipping = "shipping"
    pickup = "pickup"


class OrderStatus(str, Enum):
    waiting = "waiting"
    paid = "paid"
    accepted = "accepted"
