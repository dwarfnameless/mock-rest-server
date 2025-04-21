from typing import Annotated

from pydantic import BaseModel, Field


class ErrorModel(BaseModel):
    """Модель для представления ошибок API.

    Attributes:
        detail (str): Описание ошибки. Например, "Мок-данные не найдены".
    """

    detail: Annotated[str, Field(description="Описание ошибки", examples=["Мок-данные не найдены", "Ошибка валидации"])]
