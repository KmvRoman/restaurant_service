from dataclasses import dataclass

from src.domain.order.entities.order import Location
from src.domain.restaurant.entities.restaurant_view import RestaurantId


@dataclass
class ReadNearestLocationDtoInput:
    restaurant_id: RestaurantId
    user_location: Location


@dataclass
class ReadNearestLocationDtoOutput:
    address: str
    restaurant_location_id: int
