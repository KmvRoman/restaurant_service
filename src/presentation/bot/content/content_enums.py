from enum import Enum


class ExistingTypes(str, Enum):
    TimePeriod = "TimePeriod"
    DateTime = "DateTime"
    Amount = "Amount"
    Text = "Text"
