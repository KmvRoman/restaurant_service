from dataclasses import dataclass
from typing import Optional, NewType

from src.domain.user.constants.user import Member, Language

UserId = NewType("UserId", int)


@dataclass
class User:
    id: Optional[UserId]
    name: str
    phone: Optional[str]
    member: Member
    language: Language
