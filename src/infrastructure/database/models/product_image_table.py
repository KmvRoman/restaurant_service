from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, VARCHAR, ForeignKey

from src.infrastructure.database.models.base import Base


class ProductImageTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    product_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="producttable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    image: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
