from pydantic import BaseModel, Field


class ErrorModel(BaseModel):
    detail: str = Field(
        ...,
        description="Описание ошибки",
        example="Мок-данные не найдены",
    )
