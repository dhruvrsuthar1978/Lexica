"""Database engine lifecycle."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()

engine: AsyncEngine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    future=True,
)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_engine() -> AsyncGenerator[AsyncEngine, None]:
    """FastAPI dependency returning the application engine."""
    yield engine


async def dispose_engine() -> None:
    """Close database connections on shutdown."""
    await engine.dispose()
