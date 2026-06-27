from datetime import datetime, timezone

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncEngine

from app.db.query_logs import query_logs


class QueryLogger:
    """Persist query audit events to the application database."""

    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine

    async def log(
        self,
        question: str,
        generated_sql: str | None,
        success: bool,
        row_count: int | None,
        execution_time: float | None,
        error_message: str | None,
        client_key: str | None,
        request_id: str | None,
    ) -> None:
        payload = {
            "created_at": datetime.now(timezone.utc),
            "question": question,
            "generated_sql": generated_sql,
            "success": success,
            "row_count": row_count,
            "execution_time": execution_time,
            "error_message": error_message,
            "client_key": client_key,
            "request_id": request_id,
        }

        async with self._engine.begin() as connection:
            await connection.execute(insert(query_logs).values(**payload))

    async def fetch_recent_logs(self, limit: int = 25) -> list[dict[str, object | None]]:
        query = select(query_logs).order_by(query_logs.c.created_at.desc()).limit(limit)
        async with self._engine.connect() as connection:
            result = await connection.execute(query)
            return [dict(row._mapping) for row in result.fetchall()]
