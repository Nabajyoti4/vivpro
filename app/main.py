from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError


from app.routes.v1.api_v1 import api_router
from app.core.config import settings
from app.utils.middleware import log_request_middleware
from app.utils.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler,
)

app = FastAPI()

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Register middleware
app.middleware("http")(log_request_middleware)

# Register exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)


@app.get("/health-check")
def health_check():
    return JSONResponse({"message": "Hello, world!"}, status_code=status.HTTP_200_OK)


app.include_router(api_router)
