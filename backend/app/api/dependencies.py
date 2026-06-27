"""FastAPI dependency wiring."""

from functools import lru_cache

from app.core.config import get_settings
from app.core.rate_limit import InMemoryRateLimiter, NoopRateLimiter, RateLimiter
from app.db.engine import engine
from app.services.llm_client import LLMClient
from app.services.prompt_builder import PromptBuilder
from app.services.query_logger import QueryLogger
from app.services.query_service import QueryService
from app.services.schema_loader import SchemaLoader
from app.services.sql_executor import SQLExecutor
from app.services.sql_validator import SQLValidator


@lru_cache
def get_schema_loader() -> SchemaLoader:
    """Return the singleton schema loader."""
    settings = get_settings()
    return SchemaLoader(engine, cache_ttl_seconds=settings.schema_cache_ttl_seconds)


@lru_cache
def get_rate_limiter() -> RateLimiter:
    """Return the configured rate limiter hook."""
    settings = get_settings()
    if settings.enable_rate_limiting:
        return InMemoryRateLimiter(
            requests=settings.rate_limit_requests,
            window_seconds=settings.rate_limit_window_seconds,
        )
    return NoopRateLimiter()


@lru_cache
def get_query_logger() -> QueryLogger:
    """Return the singleton query logger."""
    return QueryLogger(engine)


def get_query_service() -> QueryService:
    """Build the query service dependency."""
    settings = get_settings()
    return QueryService(
        schema_loader=get_schema_loader(),
        prompt_builder=PromptBuilder(settings.sql_dialect),
        llm_client=LLMClient(settings),
        sql_validator=SQLValidator(settings.sql_dialect),
        sql_executor=SQLExecutor(engine),
    )
