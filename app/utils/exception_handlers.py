from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logger_config import api_logger


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []

    api_logger.error(f"Validation exception: {exc.errors()}")
    for error in exc.errors():
        column_name = error["loc"][-1]  # Extract the last element as the column name
        detail = {"field": column_name, "message": error["msg"]}
        errors.append(detail)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"errors": errors}),
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    api_logger.error(f"HTTP exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"message": exc.detail}),
    )


async def global_exception_handler(request: Request, exc: Exception):
    api_logger.exception(f"HTTP Global exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"message": "Internal server error"}),
    )
