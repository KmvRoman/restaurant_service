from dataclasses import dataclass

from src.domain.user.entities.user import User


@dataclass
class UpdateUserPhoneDtoInput:
    user: User
    phone: str
