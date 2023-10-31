from enum import Enum


class ConcretePaymentType(str, Enum):
    cache: str
    payme: str
    click: str


class ConcretePaymentTypeRu(ConcretePaymentType):
    cache = "💵 Наличными"
    payme = "💳 Payme"
    click = "💳 Click"


class ConcretePaymentTypeUz(ConcretePaymentType):
    cache = "💵 Наличными"
    payme = "💳 Payme"
    click = "💳 Click"
