from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey, FLOAT

from src.infrastructure.database.models.base import Base


class ShippingLocationTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    shipping_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="shippingordertable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    latitude: Mapped[float] = mapped_column(FLOAT, nullable=False)
    longitude: Mapped[float] = mapped_column(FLOAT, nullable=False)
