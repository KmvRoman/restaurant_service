from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, VARCHAR, ForeignKey

from src.domain.user.constants.user import Language
from src.infrastructure.database.models.base import Base


class ProductNameTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    product_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="producttable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    language: Mapped[Language] = mapped_column(nullable=False)
