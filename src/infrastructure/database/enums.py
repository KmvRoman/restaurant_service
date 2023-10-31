from enum import Enum


class TelegramStatus(str, Enum):
    active = "active"
    block = "block"
