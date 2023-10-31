from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey, INTEGER

from src.infrastructure.database.models.base import Base


class ProductBasketModificationTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    product_basket_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="productbaskettable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    modification: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="productpricetable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
