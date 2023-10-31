from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey

from src.domain.restaurant.constants.constants import MenuProductStatus
from src.infrastructure.database.models.base import Base


class MenuProductTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    location_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="restaurantlocationstable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    category_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="categoriestable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    product_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="producttable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    status: Mapped[MenuProductStatus] = mapped_column(nullable=False)
