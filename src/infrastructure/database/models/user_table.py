from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BIGINT, Identity, VARCHAR

from src.domain.user.constants.user import Member, Language
from src.infrastructure.database.models.base import Base


class UserTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, Identity(always=True, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    phone: Mapped[str] = mapped_column(VARCHAR(13), nullable=True)
    member: Mapped[Member] = mapped_column(nullable=False)
    language: Mapped[Language] = mapped_column(nullable=False)
