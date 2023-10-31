from typing import Optional

from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo

from src.domain.product.constants.product import ProductMode, ProductStatus
from src.domain.product.entities.product import ProductId
from src.domain.restaurant.entities.restaurant_view import CategoryId
from src.domain.user.constants.user import Language
from src.presentation.bot.exceptions.common import (
    ValueNotInstanceCategoryId, NameNotFoundAnyLanguages, DescriptionNotFoundAnyLanguages,
    EmptyPriceError, PriceNameNotFoundAnyLanguages, EmptyProductName,
)


class ProductNameData(BaseModel):
    name: str
    language: Language


class ProductDescriptionData(BaseModel):
    description: str
    language: Language


class ProductPriceNameData(BaseModel):
    name: str
    language: Language


class ProductPriceData(BaseModel):
    id: int
    name: Optional[list[ProductPriceNameData]]
    price: int


class ProductData(BaseModel):
    category_id: CategoryId | None = None
    photo: Optional[str] = None
    name: list[ProductNameData] = []
    description: Optional[list[ProductDescriptionData]] = []
    mode: ProductMode | None = None
    price: list[ProductPriceData] = []


class ProductEditData(BaseModel):
    id: ProductId
    photo: Optional[str]
    name: list[ProductNameData]
    description: Optional[list[ProductDescriptionData]]
    price: list[ProductPriceData]


class ProductDataValidate(BaseModel):
    category_id: CategoryId
    photo: Optional[str] = None
    name: list[ProductNameData]
    description: Optional[list[ProductDescriptionData]] = None
    mode: ProductMode
    price: list[ProductPriceData]
    status: ProductStatus

    @field_validator("category_id")
    def validate_category(cls, v: ValidationInfo):
        if isinstance(v, int):
            return v
        raise ValueNotInstanceCategoryId

    @field_validator("name")
    def validate_photo(cls, v: list[ProductNameData]):
        if len(v) == 0:
            raise EmptyProductName
        for language in list(Language):
            if language not in [i.language for i in v]:
                raise NameNotFoundAnyLanguages
        return v

    @field_validator("description")
    def validate_description(cls, v: list[ProductDescriptionData] | None):
        if len(v) == 0:
            return v
        for language in list(Language):
            if language not in [i.language for i in v]:
                raise DescriptionNotFoundAnyLanguages
        return v

    @field_validator("price")
    def validate_price(cls, v: list[ProductPriceData]):
        if len(v) == 0:
            raise EmptyPriceError
        elif len(v) == 1 and len(v[0].name) == 0:
            return v
        for language in list(Language):
            for price in v:
                if language not in [i.language for i in price.name]:
                    raise PriceNameNotFoundAnyLanguages
        return v


class ChangeProductPrice(BaseModel):
    edit: list[ProductPriceData]
    remove: list[int]
