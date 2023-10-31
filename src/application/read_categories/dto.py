from dataclasses import dataclass

from src.domain.restaurant.entities.restaurant_view import RestaurantId, CategoryId, Category
from src.domain.user.constants.user import Language


@dataclass
class ReadCategoriesDtoInput:
    restaurant_id: RestaurantId
    language: Language


@dataclass
class ReadCategoriesDtoOutput:
    categories: list[Category]

