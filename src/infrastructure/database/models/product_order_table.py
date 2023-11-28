from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, VARCHAR, ForeignKey, INTEGER

from src.infrastructure.database.models.base import Base


class ProductOrderTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    order_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="ordertable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    product_id: Mapped[float] = mapped_column(
        BIGINT,
        ForeignKey(column="producttable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    modification: Mapped[int] = mapped_column(BIGINT, nullable=False)
    count: Mapped[int] = mapped_column(INTEGER, nullable=False)
    price: Mapped[int] = mapped_column(BIGINT, nullable=False)
