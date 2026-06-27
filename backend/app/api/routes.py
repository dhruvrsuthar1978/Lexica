"""API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.api.dependencies import get_query_logger, get_query_service, get_rate_limiter
from app.core.config import get_settings
from app.core.exceptions import AuthenticationError
from app.core.rate_limit import RateLimiter
from app.schemas.query import (
    QueryLogEntry,
    QueryLogsResponse,
    QueryRequest,
    QuerySuccessResponse,
    SchemaColumn,
    SchemaForeignKey,
    SchemaResponse,
    SchemaTable,
)
from app.services.query_logger import QueryLogger
from app.services.query_service import QueryService
from app.services.schema_loader import DatabaseSchema

router = APIRouter(prefix="/api", tags=["query"])


@router.post("/query", response_model=QuerySuccessResponse)
async def query(
    request: QueryRequest,
    request_obj: Request,
    service: Annotated[QueryService, Depends(get_query_service)],
    query_logger: Annotated[QueryLogger, Depends(get_query_logger)],
    rate_limiter: Annotated[RateLimiter, Depends(get_rate_limiter)],
) -> QuerySuccessResponse:
    """Generate, validate, execute, and return SQL query results."""
    settings = get_settings()
    api_key = request_obj.headers.get("x-api-key", "").strip()

    if settings.require_api_key:
        if not api_key or api_key not in settings.api_keys:
            raise AuthenticationError("Missing or invalid API key")

    client_host = request_obj.client[0] if request_obj.client else None
    rate_limit_key = api_key or client_host or "anonymous"
    await rate_limiter.check(rate_limit_key)

    request_id = getattr(request_obj.state, "request_id", None)
    try:
        response = await service.answer(request.question)
        await query_logger.log(
            question=request.question,
            generated_sql=response.sql,
            success=True,
            row_count=response.row_count,
            execution_time=response.execution_time,
            error_message=None,
            client_key=rate_limit_key,
            request_id=request_id,
        )
        return response
    except Exception as exc:
        await query_logger.log(
            question=request.question,
            generated_sql=None,
            success=False,
            row_count=None,
            execution_time=None,
            error_message=str(exc),
            client_key=rate_limit_key,
            request_id=request_id,
        )
        raise


@router.get("/query/logs", response_model=QueryLogsResponse)
async def query_logs(
    request_obj: Request,
    query_logger: Annotated[QueryLogger, Depends(get_query_logger)],
    limit: int = 25,
) -> QueryLogsResponse:
    """Return recent persisted query audit logs."""
    settings = get_settings()
    api_key = request_obj.headers.get("x-api-key", "").strip()
    if settings.require_api_key and (not api_key or api_key not in settings.api_keys):
        raise AuthenticationError("Missing or invalid API key")

    logs = await query_logger.fetch_recent_logs(limit=limit)
    return QueryLogsResponse(logs=logs)


@router.get("/schema", response_model=SchemaResponse)
async def schema(
    service: Annotated[QueryService, Depends(get_query_service)],
) -> SchemaResponse:
    """Return the cached database schema for the frontend sidebar."""
    return _schema_to_response(await service.schema())


@router.post("/schema/refresh", response_model=SchemaResponse)
async def refresh_schema(
    service: Annotated[QueryService, Depends(get_query_service)],
) -> SchemaResponse:
    """Refresh schema metadata and return the new snapshot."""
    return _schema_to_response(await service.refresh_schema())


def _schema_to_response(schema_snapshot: DatabaseSchema) -> SchemaResponse:
    return SchemaResponse(
        tables=[
            SchemaTable(
                name=table.name,
                columns=[
                    SchemaColumn(
                        name=column.name,
                        type=column.type,
                        nullable=column.nullable,
                        default=column.default,
                    )
                    for column in table.columns
                ],
                primaryKeys=table.primary_keys,
                foreignKeys=[
                    SchemaForeignKey(
                        constrainedColumns=foreign_key.constrained_columns,
                        referredTable=foreign_key.referred_table,
                        referredColumns=foreign_key.referred_columns,
                    )
                    for foreign_key in table.foreign_keys
                ],
            )
            for table in schema_snapshot.tables
        ],
        loadedAt=schema_snapshot.loaded_at.isoformat(),
    )
