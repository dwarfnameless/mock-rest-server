import asyncio
from collections.abc import Callable, Coroutine
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from src.api.models.error_model import ErrorModel
from src.api.models.mock_model import MockWithUUID

dynamic_router = APIRouter()
"""APIRouter для динамического добавления маршрутов."""

registered_mocks: dict[str, dict[UUID, MockWithUUID]] = {}
"""Словарь зарегистрированных моков.
Ключ: строка вида 'METHOD:/uri'
Значение: словарь, где ключ — UUID, значение — MockWithUUID.
"""


def create_mock_handler(method: str, uri: str) -> Callable[[Request], Coroutine[object, object, JSONResponse]]:
    """
    Создаёт обработчик для мока по заданному HTTP-методу и URI.

    Args:
        method (str): HTTP-метод (например, 'GET', 'POST').
        uri (str): URI эндпоинта.

    Returns:
        Callable[[Request], Coroutine[object, object, JSONResponse]]: Асинхронная функция-обработчик запроса.
    """

    async def mock_handler(request: Request) -> JSONResponse:
        """
        Обрабатывает входящий запрос, возвращая сохранённый мок или ошибку.

        Args:
            request (Request): Входящий HTTP-запрос.

        Returns:
            JSONResponse: Ответ с данными мока или ошибкой.
        """
        req_uuid = request.headers.get("X-Request-ID")
        if not req_uuid:
            error = ErrorModel(detail="X-Request-ID header is required")
            return JSONResponse(status_code=400, content=error.model_dump())

        try:
            uuid_obj = UUID(req_uuid)
        except ValueError:
            error = ErrorModel(detail="X-Request-ID header must be a valid UUID")
            return JSONResponse(status_code=400, content=error.model_dump())

        route_key = f"{method}:{uri}"
        mocks_for_route = registered_mocks.get(route_key, {})

        if uuid_obj not in mocks_for_route:
            error = ErrorModel(detail="Mock data not found for this endpoint")
            return JSONResponse(status_code=404, content=error.model_dump())

        stored_mock = mocks_for_route[uuid_obj]

        if stored_mock.delay:
            await asyncio.sleep(stored_mock.delay / 1000)

        return JSONResponse(
            status_code=stored_mock.status_code,
            content=stored_mock.body,
            headers=stored_mock.headers,
        )

    return mock_handler


async def register_mock_route(mock_data: MockWithUUID) -> None:
    """
    Регистрирует новый мок и добавляет маршрут в роутер, если он ещё не существует.

    Args:
        mock_data (MockWithUUID): Данные мока, включая метод, URI, UUID и параметры ответа.

    Returns:
        None
    """
    route_key = f"{mock_data.method}:{mock_data.uri}"

    if route_key not in registered_mocks:
        registered_mocks[route_key] = {}

    registered_mocks[route_key][mock_data.uuid] = mock_data

    route_exists = any(
        isinstance(route, APIRoute) and route.path == mock_data.uri and mock_data.method.lower() in route.methods
        for route in dynamic_router.routes
    )

    if not route_exists:
        handler = create_mock_handler(mock_data.method, mock_data.uri)
        dynamic_router.add_api_route(
            path=mock_data.uri,
            endpoint=handler,
            methods=[mock_data.method],
        )
