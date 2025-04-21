from fastapi import APIRouter

from .dynamic_router import dynamic_router
from .mock_router import router as mock_router

api_router = APIRouter()
api_router.include_router(mock_router, prefix="/api/v1", tags=["mock"])
api_router.include_router(dynamic_router, tags=["dynamic"])
