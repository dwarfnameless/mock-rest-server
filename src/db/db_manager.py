"""Модуль для управления асинхронным подключением к базе данных.

Предоставляет класс DBManager для работы с асинхронной базой данных через SQLAlchemy.
Реализует паттерн Singleton для управления соединением и сессиями базы данных.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from functools import wraps
from typing import Awaitable, Callable, Concatenate, ParamSpec, Self, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .models.mock_data import Base

T = TypeVar("T")
P = ParamSpec("P")


class DBManager:
    """Менеджер для работы с асинхронной базой данных через SQLAlchemy.

    Реализует паттерн Singleton для управления соединением и сессиями базы данных.

    Атрибуты:
        _instance (DBManager | None): Единственный экземпляр класса.
        _engine: Асинхронный движок SQLAlchemy.
        _async_session_maker: Фабрика создания асинхронных сессий.

    Пример:
        Использование декоратора with_session::

            @DBManager.with_session
            async def get_user(session: AsyncSession, user_id: int):
                result = await session.get(User, user_id)
                return result
    """

    _instance = None
    _engine = None
    _async_session_maker = None

    def __new__(cls) -> Self:
        """Создает или возвращает единственный экземпляр класса DBManager.

        Returns:
            Self: Единственный экземпляр класса DBManager.

        Пример:
            Получение экземпляра DBManager::

                db = DBManager()
                assert db is DBManager()  # Всегда возвращает один и тот же экземпляр
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def initialize(self, db_url: str) -> None:
        """Инициализирует подключение к базе данных и создает таблицы.

        Args:
            db_url (str): URL для подключения к базе данных в формате SQLAlchemy.
        """
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
        """Асинхронный контекстный менеджер для работы сессией базы данных.

        Автоматически управляет жизненным циклом сессии, включая commit и rollback.

        Yields:
            AsyncSession: Асинхронная сессия SQLAlchemy.

        Raises:
            RuntimeError: Если база данных не инициализирована.
            Exception: Любая ошибка при работе с сессией приводит к откату транзакции.

        Пример:
            Использование менеджера сессий::

                async with db.session() as session:
                    result = await session.execute(select(User))
                    users = result.scalars().all()
        """
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
        """Декоратор для автоматического предоставления сессии в функцию.

        Args:
            func (Callable): Асинхронная функция, принимающая первым аргументом AsyncSession.

        Returns:
            Callable: Обертка, автоматически создающая и передающая сессию.

        Пример:
            Использование декоратора::

                @DBManager.with_session
                async def get_data(session: AsyncSession, id: int):
                    return await session.get(Model, id)
        """

        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            db = cls()
            async with db.session() as session:
                return await func(session, *args, **kwargs)

        return wrapper
