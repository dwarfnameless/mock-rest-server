from uuid import UUID

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import RequestResponseEndpoint

from src.api.models.error_model import ErrorModel
from src.services.register_mock import handle_mock_request, registered_mocks


def setup_dynamic_mock_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def dynamic_mock_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
        mock_uuid = request.headers.get("x-req-id")
        if not mock_uuid:
            return await call_next(request)

        try:
            uuid = UUID(mock_uuid)
            mock_data = registered_mocks.get(str(uuid))
            if not mock_data:
                error = ErrorModel(detail=f"Mock with UUID {mock_uuid} not found")
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content=error.model_dump(),
                )
            return await handle_mock_request(request, mock_data)
        except ValueError:
            error = ErrorModel(detail=f"Invalid UUID {mock_uuid}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=error.model_dump(),
            )
        except Exception as e:
            error = ErrorModel(detail=f"An error occurred: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=error.model_dump(),
            )
