"""API schemas for query endpoint."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class QueryRequest(BaseModel):
    """Natural language query request."""

    question: str = Field(min_length=1, max_length=2_000)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        """Normalize and validate the user question."""
        normalized = value.strip()
        if not normalized:
            raise ValueError("Question cannot be empty")
        return normalized


class QuerySuccessResponse(BaseModel):
    """Successful Text-to-SQL response."""

    model_config = ConfigDict(populate_by_name=True)

    success: bool = True
    sql: str
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int = Field(alias="rowCount")
    execution_time: float = Field(alias="executionTime")


class QueryLogEntry(BaseModel):
    """Persisted query audit record."""

    model_config = ConfigDict(populate_by_name=True)

    created_at: datetime = Field(alias="createdAt")
    question: str
    generated_sql: str | None = Field(alias="generatedSql")
    success: bool
    row_count: int | None = Field(alias="rowCount")
    execution_time: float | None = Field(alias="executionTime")
    error_message: str | None = Field(alias="errorMessage")
    client_key: str | None = Field(alias="clientKey")
    request_id: str | None = Field(alias="requestId")


class QueryLogsResponse(BaseModel):
    """Response containing persisted query logs."""

    model_config = ConfigDict(populate_by_name=True)

    success: bool = True
    logs: list[QueryLogEntry]


class SchemaColumn(BaseModel):
    """Column metadata returned to the frontend."""

    name: str
    type: str
    nullable: bool
    default: str | None = None


class SchemaForeignKey(BaseModel):
    """Foreign key metadata returned to the frontend."""

    constrained_columns: list[str] = Field(alias="constrainedColumns")
    referred_table: str = Field(alias="referredTable")
    referred_columns: list[str] = Field(alias="referredColumns")


class SchemaTable(BaseModel):
    """Table metadata returned to the frontend."""

    name: str
    columns: list[SchemaColumn]
    primary_keys: list[str] = Field(alias="primaryKeys")
    foreign_keys: list[SchemaForeignKey] = Field(alias="foreignKeys")


class SchemaResponse(BaseModel):
    """Database schema response."""

    model_config = ConfigDict(populate_by_name=True)

    success: bool = True
    tables: list[SchemaTable]
    loaded_at: str = Field(alias="loadedAt")
