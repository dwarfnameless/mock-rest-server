import sys
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.__main__ import app, lifespan

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))


@pytest.fixture
async def test_app() -> AsyncGenerator[FastAPI, None]:
    """Фикстура для инициализации приложения перед тестами."""
    async with lifespan(app):
        yield app


@pytest.fixture
def test_client(test_app: FastAPI) -> TestClient:
    """Фикстура для создания тестового клиента."""
    return TestClient(test_app)
