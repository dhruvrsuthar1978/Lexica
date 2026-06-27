import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.db.query_logs import create_query_log_table_sync, query_logs
from app.services.query_logger import QueryLogger


async def test_query_logger_persists_rows(tmp_path) -> None:
    db_path = tmp_path / "test.db"
    engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}")
    async with engine.begin() as connection:
        await connection.run_sync(create_query_log_table_sync)

    logger = QueryLogger(engine)
    await logger.log(
        question="Show users",
        generated_sql="SELECT id FROM users",
        success=True,
        row_count=5,
        execution_time=0.12,
        error_message=None,
        client_key="test-client",
        request_id="req-123",
    )

    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT question, generated_sql, success, row_count, execution_time, client_key, request_id FROM query_logs"))
        rows = result.fetchall()

    assert len(rows) == 1
    assert rows[0][0] == "Show users"
    assert rows[0][1] == "SELECT id FROM users"
    assert bool(rows[0][2]) is True
    assert rows[0][3] == 5
    assert rows[0][4] == 0.12
    assert rows[0][5] == "test-client"
    assert rows[0][6] == "req-123"
    await engine.dispose()
