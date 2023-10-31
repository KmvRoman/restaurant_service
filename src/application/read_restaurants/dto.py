from dataclasses import dataclass

from src.domain.restaurant.entities.restaurant_view import RestaurantId, LocationId


@dataclass
class ReadRestaurantsDtoInput:
    restaurant_id: RestaurantId


@dataclass
class ReadRestaurantDtoOutput:
    id: LocationId
    address: str
    latitude: float
    longitude: float
