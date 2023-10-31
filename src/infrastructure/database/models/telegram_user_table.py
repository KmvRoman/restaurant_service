from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey

from src.infrastructure.database.enums import TelegramStatus
from src.infrastructure.database.models.base import Base


class TelegramUserTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="usertable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    telegram_id: Mapped[int] = mapped_column(BIGINT, nullable=False, unique=True)
    status: Mapped[TelegramStatus] = mapped_column(nullable=False)
