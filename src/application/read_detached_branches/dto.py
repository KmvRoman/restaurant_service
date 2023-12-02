from dataclasses import dataclass

from src.domain.restaurant.entities.restaurant_view import RestaurantId, LocationId


@dataclass
class ReadDetachedBranchesDtoInput:
    restaurant_id: RestaurantId


@dataclass
class ReadDetachedBranchDtoOutput:
    location_id: LocationId
    address: str
