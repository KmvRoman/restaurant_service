from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, VARCHAR, ForeignKey

from src.domain.order.constants.order import OrderType, OrderStatus, PaymentType
from src.infrastructure.database.models.base import Base


class OrderTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="usertable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    phone: Mapped[str] = mapped_column(VARCHAR(13), nullable=False)
    order_type: Mapped[OrderType] = mapped_column(nullable=False)
    amount: Mapped[int] = mapped_column(BIGINT, nullable=False)
    payment_type: Mapped[PaymentType] = mapped_column(nullable=False)
    status: Mapped[OrderStatus] = mapped_column(nullable=False)
