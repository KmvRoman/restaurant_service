from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, VARCHAR, ForeignKey

from src.domain.user.constants.user import Language
from src.infrastructure.database.models.base import Base


class CategoryNameTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    category_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(column="categoriestable.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    category: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    language: Mapped[Language] = mapped_column(nullable=False)
