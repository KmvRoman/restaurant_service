from dataclasses import dataclass

from src.domain.product.entities.product import ProductId, ProductPrice


@dataclass
class EditProductPriceDtoInput:
    product_id: ProductId
    price: list[ProductPrice]
