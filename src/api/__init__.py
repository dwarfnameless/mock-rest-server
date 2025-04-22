"""
Модуль API роутеров.

Этот модуль содержит основной APIRouter и подключает все дочерние роутеры приложения.

Атрибуты:
    api_router (APIRouter): Основной роутер API приложения.
"""

from fastapi import APIRouter

from .mock_router import router as mock_router

api_router = APIRouter()
api_router.include_router(mock_router, prefix="/api/v1", tags=["mock"])
