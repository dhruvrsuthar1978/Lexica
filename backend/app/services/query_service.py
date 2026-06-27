"""Application service orchestrating the Text-to-SQL pipeline."""

import structlog

from app.schemas.query import QuerySuccessResponse
from app.services.llm_client import LLMClient
from app.services.prompt_builder import PromptBuilder
from app.services.schema_loader import DatabaseSchema, SchemaLoader
from app.services.sql_executor import SQLExecutor
from app.services.sql_validator import SQLValidator


class QueryService:
    """Runs the complete Text-to-SQL request pipeline."""

    def __init__(
        self,
        schema_loader: SchemaLoader,
        prompt_builder: PromptBuilder,
        llm_client: LLMClient,
        sql_validator: SQLValidator,
        sql_executor: SQLExecutor,
    ) -> None:
        self._schema_loader = schema_loader
        self._prompt_builder = prompt_builder
        self._llm_client = llm_client
        self._sql_validator = sql_validator
        self._sql_executor = sql_executor
        self._logger = structlog.get_logger("query_service")

    async def answer(self, question: str) -> QuerySuccessResponse:
        """Convert a natural language question to safe SQL and execute it."""
        schema = await self._schema_loader.get_schema()
        prompt = self._prompt_builder.build(question=question, schema=schema)
        generated_sql = await self._llm_client.generate_sql(prompt)
        validated_sql = self._sql_validator.validate(generated_sql)
        result = await self._sql_executor.execute(validated_sql)

        self._logger.info(
            "query_completed",
            question=question,
            generated_sql=validated_sql,
            execution_time=result.execution_time,
            row_count=result.row_count,
        )
        return QuerySuccessResponse(
            sql=validated_sql,
            columns=result.columns,
            rows=result.rows,
            rowCount=result.row_count,
            executionTime=result.execution_time,
        )

    async def schema(self) -> DatabaseSchema:
        """Return the cached database schema."""
        return await self._schema_loader.get_schema()

    async def refresh_schema(self) -> DatabaseSchema:
        """Refresh and return database schema metadata."""
        return await self._schema_loader.refresh_schema()
