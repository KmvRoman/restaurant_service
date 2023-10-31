from dataclasses import dataclass

from src.domain.user.constants.user import Language
from src.domain.user.entities.user import User


@dataclass
class UpdateUserLanguageDtoInput:
    user: User
    language: Language
