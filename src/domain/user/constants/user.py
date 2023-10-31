from enum import Enum


class Member(str, Enum):
    user = "user"
    administrator = "administrator"


class Language(str, Enum):
    ru = "ru"
    uz = "uz"
