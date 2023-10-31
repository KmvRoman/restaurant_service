from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey

from src.domain.order.constants.order import PaymentType
from src.infrastructure.database.models.base import Base


class PaymentTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    order_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="ordertable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    payment_type: Mapped[PaymentType] = mapped_column(nullable=False)
