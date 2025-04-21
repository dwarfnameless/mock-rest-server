import re
from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

URI_REGEX = r"^/[^/]+(/[^/]+)*$"


class MockData(BaseModel):
    """Базовая модель для определения мок-ответа.

    Содержит основные параметры, необходимые для конфигурации мок-ответа REST API,
    включая URI, HTTP метод, код статуса, заголовки и тело ответа.

    Attributes:
        uri (str): URI эндпоинта для мок-ответа.
        method (str): HTTP метод для мок-ответа.
        status_code (int): HTTP код состояния ответа.
        headers (Json): HTTP заголовки ответа.
        body (Json): Тело HTTP ответа в формате JSON.
        delay (int): Задержка ответа в миллисекундах.
    """

    uri: Annotated[
        str,
        Field(
            pattern=URI_REGEX,
            description=(
                "URI эндпоинта для мок-ответа (должен начинаться с / и может содержать дополнительные сегменты пути)"
            ),
            examples=["/api/v1/users"],
        ),
    ]
    method: Annotated[
        Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
        Field(description="HTTP метод, на который будет реагировать мок"),
    ]
    status_code: Annotated[
        int, Field(ge=100, le=699, description="HTTP код ответа (от 100 до 699)", examples=[200, 201, 400, 404, 500])
    ]

    headers: Annotated[
        dict[str, str] | None,
        Field(
            default=None,
            description="HTTP заголовки, которые будут возвращены в ответе",
            examples=[
                {"Content-Type": "application/json"},
                {"Authorization": "Bearer token123", "X-Request-ID": "abc123"},
                {"Accept": "application/json", "Cache-Control": "no-cache"},
            ],
        ),
    ]

    body: Annotated[
        dict[str, object] | None,
        Field(
            default=None,
            description="Тело ответа в формате JSON",
            examples=[
                {"users": {"id": 1, "name": "Иван Петров", "active": True}},
                {"products": [{"id": 101, "name": "Ноутбук"}, {"id": 102, "name": "Телефон"}]},
                {"error": {"code": 404, "message": "Ресурс не найден"}},
            ],
        ),
    ]

    delay: Annotated[
        int | None,
        Field(
            default=0,
            ge=0,
            le=5000,
            description="Искусственная задержка ответа в миллисекундах (от 0 до 5000)",
            examples=[0, 100, 500, 2000],
        ),
    ]

    @field_validator("uri")
    @classmethod
    def validate_uri(cls, v: str) -> str:
        """Проверяет корректность формата URI.

        Args:
            v (str): Проверяемый URI.

        Returns:
            Self: Проверенный URI.

        Raises:
            ValueError: Если URI не начинается с '/' или имеет некорректный формат.
        """
        if not v.startswith("/"):
            raise ValueError("URI должен начинаться с '/'")
        if not re.match(URI_REGEX, v):
            raise ValueError("URI должен иметь корректный формат пути")
        return v


class MockWithUUID(MockData):
    """Модель мок-ответа с уникальным идентификатором.

    Расширяет базовую модель MockData, добавляя поле UUID для уникальной идентификации мока.

    Attributes:
        uuid (UUID): Уникальный идентификатор мока.
    """

    uuid: Annotated[
        UUID,
        Field(
            description="Уникальный идентификатор для мока",
            examples=["550e8400-e29b-41d4-a716-446655440000"],
        ),
    ]


class MockModelWithDate(MockWithUUID):
    """Полная модель мок-ответа с метаданными.

    Расширяет MockWithUUID, добавляя информацию о времени создания и обновления мока.

    Attributes:
        created_at (datetime): Дата и время создания мока.
        updated_at (datetime): Дата и время последнего обновления мока.
    """

    created_at: Annotated[
        datetime,
        Field(
            description="Дата и время создания мока",
            examples=["2023-10-01T15:30:00Z"],
        ),
    ]
    updated_at: Annotated[
        datetime,
        Field(
            description="Дата и время последнего обновления мока",
            examples=["2023-10-01T15:30:00Z"],
        ),
    ]
