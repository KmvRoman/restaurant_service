from typing import NamedTuple

from src.domain.restaurant.entities.restaurant_view import RestaurantId, LocationId, CategoryId


class ShowRestaurantInfo(NamedTuple):
    restaurant_id: RestaurantId
    name: str
    description: str
    location_id: LocationId
    address: str
    latitude: float
    longitude: float


class ShowCategory(NamedTuple):
    id: CategoryId
    category: str
