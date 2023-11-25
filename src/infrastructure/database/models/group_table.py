from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey

from src.infrastructure.database.models.base import Base


class GroupTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    restaurant_location_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="restaurantlocationstable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    group_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
