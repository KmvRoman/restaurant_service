from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, INTEGER, VARCHAR

from src.infrastructure.database.models.base import Base


class RestaurantTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    token: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)
