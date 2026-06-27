"""HTTP middleware for security and observability."""

import time
import uuid
from collections.abc import Awaitable, Callable

import structlog
from fastapi import Request, Response
from starlette import status

from app.core.config import Settings
from app.core.exceptions import ErrorType, error_json


async def request_context_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Attach request ids and emit structured request logs."""
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    request.state.request_id = request_id
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)

    started = time.perf_counter()
    response = await call_next(request)
    elapsed = round(time.perf_counter() - started, 6)
    response.headers["x-request-id"] = request_id

    structlog.get_logger("http").info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        execution_time=elapsed,
    )
    return response


def make_body_size_middleware(
    settings: Settings,
) -> Callable[[Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]]:
    """Create middleware that rejects oversized requests before parsing JSON."""

    async def body_size_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > settings.max_request_bytes:
            return Response(
                content=__import__("json").dumps(
                    error_json(ErrorType.VALIDATION_ERROR, "Request body is too large")
                ),
                status_code=status.HTTP_400_BAD_REQUEST,
                media_type="application/json",
            )
        return await call_next(request)

    return body_size_middleware
