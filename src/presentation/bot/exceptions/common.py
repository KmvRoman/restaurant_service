class BotException(Exception):
    pass


class ValueNotInstanceCategoryId(BotException):
    pass


class NameNotFoundAnyLanguages(BotException):
    pass


class EmptyProductName(BotException):
    pass


class DescriptionNotFoundAnyLanguages(BotException):
    pass


class PriceNameNotFoundAnyLanguages(BotException):
    pass


class EmptyPriceError(BotException):
    pass
