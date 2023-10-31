from dataclasses import dataclass

from src.domain.restaurant.entities.restaurant_view import LocationId, RestaurantId


@dataclass
class ReadRestaurantLocationIdByAddressDtoInput:
    restaurant_id: RestaurantId
    address: str


@dataclass
class ReadRestaurantLocationIdByAddressDtoOutput:
    location_id: int
