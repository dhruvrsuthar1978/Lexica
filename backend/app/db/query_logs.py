from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    Text,
)

from app.db.engine import engine

metadata = MetaData()

query_logs = Table(
    "query_logs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("question", Text, nullable=False),
    Column("generated_sql", Text, nullable=True),
    Column("success", Boolean, nullable=False, default=False),
    Column("row_count", Integer, nullable=True),
    Column("execution_time", Float, nullable=True),
    Column("error_message", Text, nullable=True),
    Column("client_key", String(256), nullable=True),
    Column("request_id", String(128), nullable=True),
)


async def create_query_log_table() -> None:
    """Create the query log table if it does not exist."""
    async with engine.begin() as connection:
        await connection.run_sync(metadata.create_all)


def create_query_log_table_sync(sync_connection) -> None:
    """Create the query log table using a synchronous connection."""
    metadata.create_all(sync_connection)
