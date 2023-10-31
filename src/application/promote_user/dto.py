from dataclasses import dataclass

from src.domain.user.constants.user import Member
from src.domain.user.entities.user import UserId


@dataclass
class PromoteUserDtoInput:
    user_id: UserId
    member: Member
