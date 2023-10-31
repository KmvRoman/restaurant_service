from dataclasses import dataclass

from src.domain.product.entities.product import ProductId, ProductName


@dataclass
class EditProductNameDtoInput:
    product_id: ProductId
    name: list[ProductName]
