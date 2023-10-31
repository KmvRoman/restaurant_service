from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey

from src.infrastructure.database.models.base import Base


class ProductBasketTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    basket_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="baskettable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    product_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="producttable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    count: Mapped[int] = mapped_column(BIGINT, nullable=False)
