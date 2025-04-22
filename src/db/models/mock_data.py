from datetime import datetime
from typing import Literal, TypeVar
from uuid import UUID

from sqlalchemy import JSON, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

T = TypeVar("T", bound="Base")


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy.

    Используется как основа для декларативных моделей.
    """


class MockDbData(Base):
    """
    Модель данных для хранения мок-ответов в базе данных.

    Атрибуты:
        uuid (UUID): Уникальный идентификатор записи.
        uri (str): URI эндпоинта, для которого предназначен мок.
        method (Literal): HTTP-метод (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS).
        status_code (int): HTTP статус-код ответа.
        headers (dict[str, str] | None): Заголовки ответа в формате JSON.
        body (dict[str, object] | None): Тело ответа в формате JSON.
        delay (int | None): Задержка ответа в миллисекундах.
        created_at (datetime): Дата и время создания записи.
        updated_at (datetime): Дата и время последнего обновления записи.
    """

    __tablename__ = "mock_data"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    uri: Mapped[str] = mapped_column(nullable=False)
    method: Mapped[Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]] = mapped_column(nullable=False)
    status_code: Mapped[int] = mapped_column(nullable=False)
    headers: Mapped[dict[str, str]] = mapped_column(JSON, nullable=True)
    body: Mapped[dict[str, object]] = mapped_column(JSON, nullable=True)
    delay: Mapped[int] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
