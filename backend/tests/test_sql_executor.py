import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.exceptions import DatabaseExecutionError
from app.services.sql_executor import SQLExecutor


async def test_executor_returns_rows() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.execute(text("CREATE TABLE employees (id INTEGER, name TEXT)"))
        await connection.execute(text("INSERT INTO employees VALUES (1, 'Asha')"))

    result = await SQLExecutor(engine).execute("SELECT id, name FROM employees")

    assert result.columns == ["id", "name"]
    assert result.rows == [{"id": 1, "name": "Asha"}]
    assert result.row_count == 1
    await engine.dispose()


async def test_executor_blocks_writes_with_read_only_mode() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.execute(text("CREATE TABLE employees (id INTEGER)"))

    with pytest.raises(DatabaseExecutionError):
        await SQLExecutor(engine).execute("INSERT INTO employees VALUES (1)")
    await engine.dispose()
