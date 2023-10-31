from dataclasses import dataclass
from typing import Optional

from src.domain.user.constants.user import Member, Language
from src.domain.user.entities.user import UserId


@dataclass
class CreateUserDtoInput:
    name: str
    phone: Optional[str]
    language: Language
    member: Member


@dataclass
class CreateUserDtoOutput:
    user_id: UserId
