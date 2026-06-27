"""Custom exceptions and HTTP error mapping."""

from enum import StrEnum
from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette import status
from structlog import get_logger


class ErrorType(StrEnum):
    """Stable public error codes."""

    VALIDATION_ERROR = "VALIDATION_ERROR"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    UNSAFE_SQL = "UNSAFE_SQL"
    RATE_LIMITED = "RATE_LIMITED"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    LLM_UNAVAILABLE = "LLM_UNAVAILABLE"
    DATABASE_ERROR = "DATABASE_ERROR"


class ErrorBody(BaseModel):
    """Public error shape."""

    type: ErrorType
    message: str


class ErrorResponse(BaseModel):
    """Public API error response."""

    success: bool = False
    error: ErrorBody


class AppError(Exception):
    """Base application exception with a safe public message."""

    def __init__(
        self,
        message: str,
        *,
        error_type: ErrorType,
        status_code: int,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        self.status_code = status_code
        self.details = details or {}


class ValidationAppError(AppError):
    """Request or business validation failed."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message,
            error_type=ErrorType.VALIDATION_ERROR,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class UnsafeSQLError(AppError):
    """Generated SQL is not safe to execute."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message,
            error_type=ErrorType.UNSAFE_SQL,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


class LLMUnavailableError(AppError):
    """LLM provider failed or is unavailable."""

    def __init__(self, message: str = "LLM provider is unavailable") -> None:
        super().__init__(
            message,
            error_type=ErrorType.LLM_UNAVAILABLE,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )


class AuthenticationError(AppError):
    """Authentication failed or is required."""

    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(
            message,
            error_type=ErrorType.AUTHENTICATION_ERROR,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class DatabaseExecutionError(AppError):
    """Database query failed."""

    def __init__(self, message: str = "Database query failed") -> None:
        super().__init__(
            message,
            error_type=ErrorType.DATABASE_ERROR,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def error_json(error_type: ErrorType, message: str) -> dict[str, Any]:
    """Build a stable JSON error envelope."""
    return ErrorResponse(error=ErrorBody(type=error_type, message=message)).model_dump()


async def app_error_handler(_: Request, exc: Exception) -> JSONResponse:
    """Render known application errors without leaking internals."""
    if not isinstance(exc, AppError):
        return await unhandled_error_handler(_, exc)
    get_logger("errors").warning(
        "app_error",
        error_type=exc.error_type,
        message=exc.message,
        details=exc.details,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_json(exc.error_type, exc.message),
    )


async def validation_error_handler(
    _: Request, exc: Exception
) -> JSONResponse:
    """Render FastAPI/Pydantic validation errors."""
    if not isinstance(exc, RequestValidationError):
        return await unhandled_error_handler(_, exc)
    first_error = exc.errors()[0] if exc.errors() else {}
    message = str(first_error.get("msg", "Invalid request"))
    get_logger("errors").warning(
        "request_validation_failed",
        error_type=ErrorType.VALIDATION_ERROR,
        message=message,
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_json(ErrorType.VALIDATION_ERROR, message),
    )


async def unhandled_error_handler(_: Request, exc: Exception) -> JSONResponse:
    """Render unexpected failures without stack traces."""
    get_logger("errors").error("unhandled_error", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_json(ErrorType.INTERNAL_ERROR, "Internal server error"),
    )
