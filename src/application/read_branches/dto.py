from dataclasses import dataclass

from src.domain.restaurant.entities.restaurant_view import RestaurantId, LocationId


@dataclass
class ReadBranchesDtoInput:
    restaurant_id: RestaurantId


@dataclass
class ReadBranchesDtoOutput:
    location_id: LocationId
    address: str
