from datetime import datetime
from typing import Literal
from uuid import UUID

from sqlalchemy import JSON, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase): ...


class MockData(Base):
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
