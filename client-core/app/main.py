from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.routers.main import api_router
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from app.schemas.common import APIError
import logging


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Environment: {settings.ENVIRONMENT}")
logger.info(f"CORS Origins: {settings.all_cors_origins}")
# logger.info(f"Reports Base URL: {settings.REPORTS_BASE_URL}")

# Disable OpenAPI docs in production
openapi_url = (
    f"{settings.API_V1_STR}/openapi.json"
    if settings.ENVIRONMENT != "production"
    else None
)
docs_url = (
    f"{settings.API_V1_STR}/docs" if settings.ENVIRONMENT != "production" else None
)
redoc_url = (
    f"{settings.API_V1_STR}/redoc" if settings.ENVIRONMENT != "production" else None
)

app = FastAPI(
    title=settings.PROJECT_NAME,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


# Exception handler for 422 Unprocessable Entity
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=APIError(
            code="VALIDATION_ERROR",
            message="Invalid request data",
            details=[
                {"field": ".".join(map(str, error["loc"])), "message": error["msg"]}
                for error in exc.errors()
            ],
        ).model_dump(),
    )


# Exception handler for known HTTPExceptions (e.g., 403, 404)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTP error {exc.status_code}: {exc.detail}")

    # If Internal Server Error, return 500
    if exc.status_code == 500:
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=APIError(
                code="INTERNAL_ERROR",
                message="An unexpected error occurred",
                details=None,
            ).model_dump(),
        )

    # If detail is a dict and looks like our APIError structure
    if (
        isinstance(exc.detail, dict)
        and "code" in exc.detail
        and "message" in exc.detail
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,  # Already structured
        )

    # Fallback to generic HTTP error
    return JSONResponse(
        status_code=exc.status_code,
        content=APIError(
            code="ERROR", message=str(exc.detail), details=None
        ).model_dump(),
    )


# Catch-all handler for unexpected server errors
@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content=APIError(
            code="INTERNAL_ERROR", message="An unexpected error occurred", details=None
        ).model_dump(),
    )


# Health check
@app.get("/health", tags=["health_check"])
async def health() -> str:
    return "ok"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
