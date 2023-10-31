from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, ForeignKey, VARCHAR

from src.domain.user.constants.user import Language
from src.infrastructure.database.models.base import Base


class ProductPriceNameTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    price_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="productpricetable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(VARCHAR(55), nullable=False)
    language: Mapped[Language] = mapped_column(nullable=False)
