import asyncio

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.api.models.error_model import ErrorModel
from src.api.models.mock_model import MockWithUUID


async def handle_mock_request(req: Request, mock_data: MockWithUUID) -> JSONResponse:
    """
    Обрабатывает входящий HTTP-запрос и возвращает ответ на основе предоставленных данных мока.

    Args:
        req (Request): Входящий HTTP-запрос FastAPI.
        mock_data (MockWithUUID): Данные мока, содержащие параметры для ответа.

    Returns:
        JSONResponse: Ответ, соответствующий данным мока или сообщение об ошибке.

    Raises:
        None

    Примеры:
        >>> await handle_mock_request(request, mock_data)
        <JSONResponse ...>
    """
    if req.method != mock_data.method:
        error = ErrorModel(detail=f"Method {req.method} not allowed for this endpoint")
        return JSONResponse(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            content=error.model_dump(),
        )

    if req.url.path != mock_data.uri:
        error = ErrorModel(detail=f"Path {req.url.path} not allowed for this endpoint")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error.model_dump(),
        )

    if mock_data.delay:
        await asyncio.sleep(mock_data.delay / 1000)

    return JSONResponse(
        status_code=mock_data.status_code,
        content=mock_data.body if mock_data.body else None,
        headers=mock_data.headers if mock_data.headers else None,
    )
