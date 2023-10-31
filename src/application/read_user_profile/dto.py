from dataclasses import dataclass
from typing import Optional

from src.domain.user.constants.user import Member, Language
from src.domain.user.entities.user import UserId


@dataclass
class ReadUserProfileDtoInput:
    user_id: UserId


@dataclass
class ReadUserProfileDtoOutput:
    user_id: UserId
    name: str
    phone: Optional[str]
    member: Member
    language: Language
