from typing import Optional

from src.domain.product.constants.product import ProductMode, ProductStatus
from src.domain.product.entities.product import Product, ProductName, ProductDescription, ProductPrice, ProductId
from src.domain.product.exceptions.exceptions import (
    ProductNameError, ProductDescriptionError, ProductPriceNameError,
    ProductPriceNameNotExist, ProductModeError, ProductPriceNotFoundError,
    ProductNameNotFoundError, ProductDescriptionNotFound,
)
from src.domain.user.constants.user import Language


class ProductService:
    def create_product(
            self, photo: Optional[str], name: list[ProductName],
            description: Optional[list[ProductDescription]],
            mode: ProductMode, price: list[ProductPrice],
            status: ProductStatus,
    ) -> Product:
        return Product(
            id=None, photo=photo, name=name, description=description,
            mode=mode, price=price, status=status,
        )

    def edit_product_photo(self, photo: str, product: Product) -> Product:
        product.photo = photo
        return product

    def edit_product_name(self, name: list[ProductName], product: Product) -> Product:
        self.check_name(name=name)
        product.name = name
        return product

    def edit_product_description(
            self, description: Optional[list[ProductDescription]],
            product: Product,
    ) -> Product:
        if description is None:
            raise ProductDescriptionNotFound
        self.check_description(description=description)
        product.description = description
        return product

    def edit_product_price(self, price: list[ProductPrice], product: Product) -> Product:
        self.check_price(price=price, product=product)
        product.price = price
        return product

    def delete_product(self, product: Product) -> ProductId:
        product.status = ProductStatus
        return product.id

    def get_from_stop_list(self, product: Product) -> Product:
        product.status = ProductStatus.active
        return product

    def check_name(self, name: list[ProductName]) -> None:
        if name is None:
            raise ProductNameNotFoundError
        for pr in name:
            if pr.language not in list(Language):
                raise ProductNameError

    def check_description(self, description: Optional[list[ProductDescription]]) -> None:
        for des in description:
            if des.language not in list(Language):
                raise ProductDescriptionError

    def check_price(self, price: list[ProductPrice], product: Product) -> None:
        if price is None:
            raise ProductPriceNotFoundError
        if product.mode == ProductMode.extend:
            if len(price) == 1:
                raise ProductModeError
            for pr in price:
                if pr.name is None or len(pr.name) == 0:
                    raise ProductPriceNameNotExist
                for price_name in pr.name:
                    if price_name.language not in list(Language):
                        raise ProductPriceNameError
        elif product.mode == ProductMode.default:
            if len(price) > 1:
                raise ProductModeError
            if len(price[0].name) != 0:
                raise ProductPriceNameError
        else:
            raise ProductModeError
