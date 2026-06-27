"""Database schema introspection with in-memory caching."""

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncEngine


@dataclass(frozen=True)
class ColumnInfo:
    """Column metadata."""

    name: str
    type: str
    nullable: bool
    default: str | None = None


@dataclass(frozen=True)
class ForeignKeyInfo:
    """Foreign key relationship metadata."""

    constrained_columns: list[str]
    referred_table: str
    referred_columns: list[str]


@dataclass(frozen=True)
class TableInfo:
    """Table metadata."""

    name: str
    columns: list[ColumnInfo]
    primary_keys: list[str] = field(default_factory=list)
    foreign_keys: list[ForeignKeyInfo] = field(default_factory=list)


@dataclass(frozen=True)
class DatabaseSchema:
    """Database schema snapshot."""

    tables: list[TableInfo]
    loaded_at: datetime

    def to_prompt_text(self) -> str:
        """Render compact schema text for LLM prompts."""
        lines: list[str] = []
        for table in self.tables:
            lines.append(f"Table: {table.name}")
            for column in table.columns:
                nullable = "nullable" if column.nullable else "not null"
                lines.append(f"  - {column.name}: {column.type}, {nullable}")
            if table.primary_keys:
                lines.append(f"  Primary key: {', '.join(table.primary_keys)}")
            for foreign_key in table.foreign_keys:
                left = ", ".join(foreign_key.constrained_columns)
                right = ", ".join(foreign_key.referred_columns)
                lines.append(
                    f"  Foreign key: {table.name}({left}) -> "
                    f"{foreign_key.referred_table}({right})"
                )
        return "\n".join(lines)


class SchemaLoader:
    """Introspects and caches database schema metadata."""

    def __init__(self, engine: AsyncEngine, cache_ttl_seconds: int = 300) -> None:
        self._engine = engine
        self._cache: DatabaseSchema | None = None
        self._cache_ttl_seconds = cache_ttl_seconds

    async def get_schema(self) -> DatabaseSchema:
        """Return cached schema, loading it on first use or when stale."""
        if self._cache is None or self._is_cache_stale():
            self._cache = await self.refresh_schema()
        return self._cache

    def _is_cache_stale(self) -> bool:
        if self._cache is None:
            return True
        return datetime.now(UTC) - self._cache.loaded_at >= timedelta(
            seconds=self._cache_ttl_seconds
        )

    async def refresh_schema(self) -> DatabaseSchema:
        """Reload schema metadata from the database."""
        async with self._engine.connect() as connection:
            schema = await connection.run_sync(self._inspect_schema)
        self._cache = schema
        return schema

    @staticmethod
    def _inspect_schema(sync_connection: Any) -> DatabaseSchema:
        inspector = inspect(sync_connection)
        tables: list[TableInfo] = []

        for table_name in inspector.get_table_names():
            columns = [
                ColumnInfo(
                    name=str(column["name"]),
                    type=str(column["type"]),
                    nullable=bool(column.get("nullable", True)),
                    default=(
                        None
                        if column.get("default") is None
                        else str(column.get("default"))
                    ),
                )
                for column in inspector.get_columns(table_name)
            ]
            primary_key = inspector.get_pk_constraint(table_name)
            foreign_keys = [
                ForeignKeyInfo(
                    constrained_columns=list(fk.get("constrained_columns") or []),
                    referred_table=str(fk.get("referred_table")),
                    referred_columns=list(fk.get("referred_columns") or []),
                )
                for fk in inspector.get_foreign_keys(table_name)
            ]
            tables.append(
                TableInfo(
                    name=table_name,
                    columns=columns,
                    primary_keys=list(primary_key.get("constrained_columns") or []),
                    foreign_keys=foreign_keys,
                )
            )

        return DatabaseSchema(tables=tables, loaded_at=datetime.now(UTC))
