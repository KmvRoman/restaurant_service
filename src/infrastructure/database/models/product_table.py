from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity

from src.domain.product.constants.product import ProductMode, ProductStatus
from src.infrastructure.database.models.base import Base


class ProductTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    mode: Mapped[ProductMode] = mapped_column(nullable=False)
    status: Mapped[ProductStatus] = mapped_column(nullable=False)
