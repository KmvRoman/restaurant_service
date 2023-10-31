from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, VARCHAR, ForeignKey, FLOAT

from src.infrastructure.database.models.base import Base


class ShippingOrderTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    order_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="ordertable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    address: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    comment: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    shipping_length: Mapped[float] = mapped_column(FLOAT, nullable=False)
    total_amount: Mapped[int] = mapped_column(BIGINT, nullable=False)
