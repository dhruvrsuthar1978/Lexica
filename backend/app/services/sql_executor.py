"""Async read-only SQL execution."""

import time
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine

from app.core.exceptions import DatabaseExecutionError


@dataclass(frozen=True)
class QueryResult:
    """Database query result payload."""

    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int
    execution_time: float


class SQLExecutor:
    """Executes validated SQL in a read-only transaction."""

    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine

    async def execute(self, sql: str) -> QueryResult:
        """Execute SQL and return rows with timing metadata."""
        started = time.perf_counter()
        async with self._engine.connect() as connection:
            transaction = await connection.begin()
            try:
                dialect_name = connection.dialect.name
                if dialect_name == "postgresql":
                    await connection.execute(text("SET TRANSACTION READ ONLY"))
                elif dialect_name == "sqlite":
                    await connection.execute(text("PRAGMA query_only = ON"))

                result = await connection.execute(text(sql))
                columns = list(result.keys())
                rows = [
                    {key: _json_safe(value) for key, value in row._mapping.items()}
                    for row in result.fetchall()
                ]
                await transaction.rollback()
            except SQLAlchemyError as exc:
                await transaction.rollback()
                raise DatabaseExecutionError(str(exc)) from exc
            finally:
                if connection.dialect.name == "sqlite":
                    await connection.execute(text("PRAGMA query_only = OFF"))

        elapsed = round(time.perf_counter() - started, 6)
        return QueryResult(
            columns=columns,
            rows=rows,
            row_count=len(rows),
            execution_time=elapsed,
        )


def _json_safe(value: Any) -> Any:
    """Convert common DB values to JSON-serializable values."""
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    return value
