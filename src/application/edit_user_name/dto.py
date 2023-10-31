from dataclasses import dataclass

from src.domain.user.entities.user import User


@dataclass
class EditUserNameDtoInput:
    user: User
    name: str
