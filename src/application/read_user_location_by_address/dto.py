from dataclasses import dataclass

from src.domain.order.entities.order import Location
from src.domain.user.entities.user import UserId


@dataclass
class ReadUserLocationByAddressDtoInput:
    user_id: UserId
    address: str


@dataclass
class ReadUserLocationByAddressDtoOutput:
    location: Location
