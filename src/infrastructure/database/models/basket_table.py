from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey

from src.domain.order.constants.basket import BasketStatus
from src.infrastructure.database.models.base import Base


class BasketTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="usertable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    status: Mapped[BasketStatus] = mapped_column(nullable=False)
