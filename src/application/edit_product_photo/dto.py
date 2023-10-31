from dataclasses import dataclass

from src.domain.product.entities.product import ProductId


@dataclass
class EditProductPhotoDtoInput:
    product_id: ProductId
    photo: str
