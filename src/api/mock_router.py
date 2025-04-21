from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Query
from fastapi.responses import JSONResponse

from src.api.models.error_model import ErrorModel
from src.api.models.mock_model import MockData, MockModelWithDate
from src.services.mock_service import create_mock_data, delete_mock_data, get_all_mock_data, get_mock_data_by_uuid

router = APIRouter()


@router.get(
    "/mock",
    response_model=list[MockModelWithDate] | MockModelWithDate,
    responses={404: {"model": ErrorModel, "description": "Мок-данные не найдены"}},
)
async def get_mock(
    uuid: Annotated[UUID | None, Query(description="UUID мок-данных")] = None,
) -> list[MockModelWithDate] | MockModelWithDate | JSONResponse:
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


@router.post("/mock", response_model=MockModelWithDate)
async def create_mock(mock: MockData) -> MockModelWithDate:
    return await create_mock_data(mock)


@router.delete("/mock")
async def delete_mock(uuid: UUID) -> JSONResponse:
    res = await delete_mock_data(uuid)
    if not res:
        error = ErrorModel(detail="Мок-данные с указанным UUID не найдены")
        return JSONResponse(status_code=404, content=error.model_dump())
    return JSONResponse(status_code=200, content=None)
