from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from functools import wraps
from typing import Awaitable, Callable, Concatenate, ParamSpec, Self, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .models.mock_data import Base

T = TypeVar("T")
P = ParamSpec("P")


class DBManager:
    _instance = None
    _engine = None
    _async_session_maker = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize(self, db_url: str) -> None:
        if not self._engine:
            self._engine = create_async_engine(
                db_url,
                echo=True,
                future=True,
            )

            self._async_session_maker = async_sessionmaker(
                self._engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )

            async with self._engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        if not self._async_session_maker:
            raise RuntimeError("Database not initialized. Call initialize() first")

        async with self._async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @classmethod
    def with_session(cls, func: Callable[Concatenate[AsyncSession, P], Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            db = cls()
            async with db.session() as session:
                return await func(session, *args, **kwargs)

        return wrapper
