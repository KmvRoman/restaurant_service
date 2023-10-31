from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey

from src.infrastructure.database.models.base import Base


class CategoriesTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="restauranttable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
