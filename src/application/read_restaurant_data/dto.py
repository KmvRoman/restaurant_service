from dataclasses import dataclass

from src.domain.restaurant.entities.restaurant_view import RestaurantId, RestaurantLocation
from src.domain.user.constants.user import Language


@dataclass
class ReadRestaurantDataDtoInput:
    restaurant_id: RestaurantId
    language: Language


@dataclass
class ReadRestaurantDataDtoOutput:
    name: str
    description: str
    locations: [RestaurantLocation]