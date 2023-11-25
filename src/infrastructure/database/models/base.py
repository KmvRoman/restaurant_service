from typing import Optional, cast, Type

from sqlalchemy.orm.decl_api import registry, DeclarativeMeta, declared_attr, has_inherited_table


class Base(metaclass=DeclarativeMeta):
    """Declarative meta for mypy"""

    __abstract__ = True
    __mapper_args__ = {"eager_defaults": True}

    # these are supplied by the sqlalchemy-stubs or sqlalchemy2-stubs, so may be omitted
    # when they are installed
    registry = registry()
    metadata = registry.metadata

    @declared_attr
    def __tablename__(self) -> Optional[str]:
        if not has_inherited_table(cast(Type[Base], self)):
            return cast(Type[Base], self).__qualname__.lower()
        return None
