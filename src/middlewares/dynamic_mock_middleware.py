from uuid import UUID

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import RequestResponseEndpoint

from src.api.models.error_model import ErrorModel
from src.services.handle_mock_request import handle_mock_request
from src.services.mock_service import get_last_mock_data_by_uri_and_method, get_mock_data_by_uuid


def setup_dynamic_mock_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def dynamic_mock_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            mock_uuid = request.headers.get("x-req-id")

            if mock_uuid:
                uuid = UUID(mock_uuid)
                mock_data = await get_mock_data_by_uuid(uuid)
                if not mock_data:
                    error = ErrorModel(detail=f"Mock with UUID {mock_uuid} not found")
                    return JSONResponse(
                        status_code=status.HTTP_404_NOT_FOUND,
                        content=error.model_dump(),
                    )
                return await handle_mock_request(request, mock_data)

            mock_data = await get_last_mock_data_by_uri_and_method(
                uri=request.url.path,
                method=request.method,
            )

            if mock_data:
                return await handle_mock_request(request, mock_data)

            return await call_next(request)

        except ValueError:
            error = ErrorModel(detail=f"Invalid UUID format: {mock_uuid}")
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
