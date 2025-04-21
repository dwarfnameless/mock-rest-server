from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status
from fastapi.params import Query
from fastapi.responses import JSONResponse

from src.api.models.error_model import ErrorModel
from src.api.models.mock_model import MockData, MockModelWithDate
from src.services.mock_service import create_mock_data, delete_mock_data, get_all_mock_data, get_mock_data_by_uuid

from .dynamic_router import register_mock_route

router = APIRouter()


@router.get(
    "/mock",
    response_model=list[MockModelWithDate] | MockModelWithDate,
    responses={404: {"model": ErrorModel, "description": "Мок-данные не найдены"}},
)
async def get_mock(
    uuid: Annotated[UUID | None, Query(description="UUID мок-данных")] = None,
) -> list[MockModelWithDate] | MockModelWithDate | JSONResponse:
    """
    Получить мок-данные по UUID или список всех мок-данных.

    Args:
        uuid (UUID | None): UUID мок-данных. Если не указан, возвращается список всех мок-данных.

    Returns:
        list[MockModelWithDate] | MockModelWithDate | JSONResponse:
            - Если uuid не указан: список всех мок-данных или ошибка 404, если данных нет.
            - Если uuid указан: объект мок-данных или ошибка 404, если не найден.
    """
    if uuid is None:
        mocks = await get_all_mock_data()
        if not mocks:
            error = ErrorModel(detail="Мок-данные не найдены")
            return JSONResponse(status_code=404, content=error.model_dump())
        return mocks

    mock = await get_mock_data_by_uuid(uuid)
    if mock is None:
        error = ErrorModel(detail="Мок-данные с указанным UUID не найдены")
        return JSONResponse(status_code=404, content=error.model_dump())
    return mock


@router.post("/mock", response_model=MockModelWithDate, status_code=status.HTTP_201_CREATED)
async def create_mock(mock: MockData) -> MockModelWithDate:
    """
    Создать новые мок-данные.

    Args:
        mock (MockData): Данные для создания нового мока.

    Returns:
        MockModelWithDate: Созданный объект мок-данных с датой.
    """
    mock_data = await create_mock_data(mock)
    await register_mock_route(mock_data)
    return mock_data


@router.delete("/mock")
async def delete_mock(uuid: UUID) -> JSONResponse:
    """
    Удалить мок-данные по UUID.

    Args:
        uuid (UUID): UUID мок-данных для удаления.

    Returns:
        JSONResponse:
            - 200, если удаление прошло успешно.
            - 404, если мок-данные с указанным UUID не найдены.
    """
    res = await delete_mock_data(uuid)
    if not res:
        error = ErrorModel(detail="Мок-данные с указанным UUID не найдены")
        return JSONResponse(status_code=404, content=error.model_dump())
    return JSONResponse(status_code=200, content=None)
