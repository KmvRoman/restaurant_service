from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey, VARCHAR

from src.domain.restaurant.constants.constants import MenuProductStatus
from src.domain.user.constants.user import Language
from src.infrastructure.database.models.base import Base


class RestaurantNameDescriptionTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="restauranttable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    description: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)
    language: Mapped[Language] = mapped_column(nullable=False)
