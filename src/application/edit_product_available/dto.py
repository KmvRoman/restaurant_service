from dataclasses import dataclass

from src.domain.restaurant.constants.constants import MenuProductStatus


@dataclass
class EditProductAvailableDtoInput:
    menu_product_id: int


@dataclass
class EditProductAvailableDtoOutput:
    status: MenuProductStatus
