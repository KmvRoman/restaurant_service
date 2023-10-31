from dataclasses import dataclass

from src.domain.restaurant.entities.restaurant_view import LocationId
from src.domain.user.constants.user import Language


@dataclass
class ReadStopListDtoInput:
    location_id: LocationId
    language: Language


@dataclass
class ReadStopListDtoOutput:
    menu_product_id: int
    name: str
