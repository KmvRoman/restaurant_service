from dataclasses import dataclass

from src.domain.user.entities.user import UserId


@dataclass
class GetUserAddressesDtoInput:
    user_id: UserId


@dataclass
class GetUserAddressesDtoOutput:
    addresses: list[str]
