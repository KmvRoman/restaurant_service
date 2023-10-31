from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, VARCHAR, ForeignKey

from src.infrastructure.database.models.base import Base


class RestaurantBannerTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="restauranttable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    banner_url: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)
