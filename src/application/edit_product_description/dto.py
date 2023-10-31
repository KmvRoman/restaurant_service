from dataclasses import dataclass

from src.domain.product.entities.product import ProductId, ProductDescription


@dataclass
class EditProductDescriptionDtoInput:
    product_id: ProductId
    description: list[ProductDescription]
