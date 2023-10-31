from dataclasses import dataclass

from src.domain.order.entities.order import Location
from src.domain.restaurant.entities.restaurant_view import LocationId


@dataclass
class ReadLocationDtoInput:
    location_id: LocationId


@dataclass
class ReadLocationDtoOutput:
    address: str
    location: Location
