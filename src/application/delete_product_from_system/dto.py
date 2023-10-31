from dataclasses import dataclass

from src.domain.product.entities.product import ProductId


@dataclass
class DeleteProductDtoInput:
    product_id: ProductId
