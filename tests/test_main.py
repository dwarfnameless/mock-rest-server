import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_root_endpoint(test_client: TestClient) -> None:
    """Тест корневого эндпоинта."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_lifespan() -> None:
    """Тест работы контекстного менеджера жизненного цикла."""
    from src.__main__ import app, lifespan

    async with lifespan(app):
        assert True


@pytest.mark.asyncio
async def test_cors_headers(test_client: TestClient) -> None:
    """Тест наличия CORS заголовков."""
    response = test_client.options(
        "/",
        headers={
            "Origin": "*",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "*",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "*"
    assert response.headers["access-control-allow-credentials"] == "true"
    assert any(
        method in response.headers["access-control-allow-methods"]
        for method in ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    )
    assert response.headers["access-control-allow-headers"] == "*"


@pytest.mark.asyncio
async def test_db_initialization(test_app: FastAPI) -> None:
    """Тест инициализации базы данных."""
    from sqlalchemy import text

    from src.db import DBManager
    from src.db.models.mock_data import Base

    db_manager = DBManager()

    assert db_manager._engine is not None

    async with db_manager._engine.begin() as conn:
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = {row[0] for row in result}

        model_tables = {mapper.class_.__tablename__ for mapper in Base.registry.mappers}

        assert all(table in tables for table in model_tables)

        result = await conn.execute(text("PRAGMA table_info(mock_data)"))
        mock_data_columns = {row[1] for row in result}
        expected_columns = {
            "uuid",
            "uri",
            "method",
            "status_code",
            "headers",
            "body",
            "delay",
            "created_at",
            "updated_at",
        }
        assert mock_data_columns == expected_columns


@pytest.mark.asyncio
async def test_routes_registration(test_app: FastAPI) -> None:
    """Тест регистрации всех роутеров."""
    from fastapi.routing import APIRoute

    routes = [route for route in test_app.routes if isinstance(route, APIRoute)]

    root_route = next((route for route in routes if route.path == "/"), None)
    assert root_route is not None
    assert "GET" in root_route.methods

    mock_routes = [route for route in routes if route.path == "/api/v1/mock"]
    assert mock_routes, "Не найдены роуты для работы с моками"

    mock_methods = set()
    for route in mock_routes:
        mock_methods.update(route.methods)

    assert "GET" in mock_methods, "GET метод не доступен для /api/v1/mock"
    assert "POST" in mock_methods, "POST метод не доступен для /api/v1/mock"
    assert "DELETE" in mock_methods, "DELETE метод не доступен для /api/v1/mock"
