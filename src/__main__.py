from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import api_router
from src.db import initialize_db
from src.middlewares.dynamic_mock_middleware import setup_dynamic_mock_middleware
from src.settings import config


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Контекстный менеджер жизненного цикла приложения FastAPI.

    Инициализирует базу данных перед запуском приложения.

    Args:
        app (FastAPI): Экземпляр приложения FastAPI.

    Yields:
        None: После инициализации базы данных управление возвращается FastAPI.
    """
    await initialize_db()

    yield


app = FastAPI(
    title=config.APP_TITLE,
    description=config.APP_VERSION,
    version=config.APP_DESCRIPTION,
    lifespan=lifespan,
)
"""
Экземпляр FastAPI приложения.

Attributes:
    title (str): Название приложения.
    description (str): Описание приложения.
    version (str): Версия приложения.
    lifespan (Callable): Контекстный менеджер жизненного цикла приложения.

Конфигурируется с помощью параметров из файла настроек и включает жизненный цикл, CORS и маршруты API.
"""

setup_dynamic_mock_middleware(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    """
    Корневой маршрут API.

    Returns:
        dict[str, str]: Сообщение приветствия.
    """
    return {"message": "Hello World"}


if __name__ == "__main__":
    """
    Точка входа для запуска приложения с помощью uvicorn.

    Использует параметры хоста и порта из конфигурации.

    Example:
        python -m src.__main__
    """
    import uvicorn

    uvicorn.run(
        app,
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
    )
