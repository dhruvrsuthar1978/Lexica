from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.services.schema_loader import SchemaLoader


async def test_schema_loader_introspects_tables() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.execute(
            text("CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT)")
        )
        await connection.execute(
            text(
                "CREATE TABLE employees ("
                "id INTEGER PRIMARY KEY, "
                "department_id INTEGER REFERENCES departments(id), "
                "name TEXT NOT NULL)"
            )
        )

    schema = await SchemaLoader(engine).get_schema()

    assert {table.name for table in schema.tables} == {"departments", "employees"}
    employees = next(table for table in schema.tables if table.name == "employees")
    assert "id" in employees.primary_keys
    assert employees.foreign_keys[0].referred_table == "departments"
    await engine.dispose()
