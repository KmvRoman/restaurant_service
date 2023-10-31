import typing
from abc import ABC
from sqlalchemy.ext.asyncio import AsyncSessionTransaction, AsyncSession
from sqlalchemy.orm import sessionmaker

Model = typing.TypeVar("Model")
TransactionContext = typing.AsyncContextManager[AsyncSessionTransaction]


class BaseRepository(ABC, typing.Generic[Model]):
    def __init__(self, session_or_pool: sessionmaker | AsyncSession) -> None:
        if isinstance(session_or_pool, sessionmaker):
            self.session: AsyncSession = typing.cast(AsyncSession, session_or_pool())
        else:
            self.session = session_or_pool
