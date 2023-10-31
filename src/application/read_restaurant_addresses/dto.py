from dataclasses import dataclass

from src.domain.restaurant.entities.restaurant_view import RestaurantId


@dataclass
class ReadRestaurantAddressesDtoInput:
    restaurant_id: RestaurantId


@dataclass
class ReadRestaurantAddressesDtoOutput:
    addresses: list[str]
