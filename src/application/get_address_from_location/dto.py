from dataclasses import dataclass

from src.domain.order.entities.order import Location


@dataclass
class GetAddressFromLocationDtoInput:
    location: Location


@dataclass
class GetAddressFromLocationDtoOutput:
    address: str
