from fastapi import APIRouter

from .mock import router as mock_router

api_router = APIRouter()
api_router.include_router(mock_router, prefix="/api/v1", tags=["mock"])
