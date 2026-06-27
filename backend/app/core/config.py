"""Application configuration loaded from environment variables."""

from functools import lru_cache
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Settings(BaseModel):
    """Runtime settings for the backend.

    Values are read from `.env` and process environment variables. Defaults keep
    local development bootable while deployment can require stricter env checks.
    """

    model_config = ConfigDict(extra="ignore")

    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    database_url: str = Field(
        default="sqlite+aiosqlite:///./text_to_sql.db", alias="DATABASE_URL"
    )
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    model_name: str = Field(default="gpt-4.1-mini", alias="MODEL_NAME")
    base_url: str = Field(default="https://api.openai.com/v1", alias="BASE_URL")
    temperature: float = Field(default=0.0, alias="TEMPERATURE")
    max_tokens: int = Field(default=512, alias="MAX_TOKENS")
    request_timeout_seconds: float = Field(
        default=30.0, alias="REQUEST_TIMEOUT_SECONDS"
    )
    llm_retries: int = Field(default=2, alias="LLM_RETRIES")
    cors_origins: list[str] = Field(default_factory=lambda: ["*"], alias="CORS_ORIGINS")
    max_question_length: int = Field(default=2_000, alias="MAX_QUESTION_LENGTH")
    max_request_bytes: int = Field(default=16_384, alias="MAX_REQUEST_BYTES")
    schema_cache_ttl_seconds: int = Field(default=300, alias="SCHEMA_CACHE_TTL_SECONDS")
    enable_rate_limiting: bool = Field(default=False, alias="ENABLE_RATE_LIMITING")
    rate_limit_requests: int = Field(default=60, alias="RATE_LIMIT_REQUESTS")
    rate_limit_window_seconds: int = Field(default=60, alias="RATE_LIMIT_WINDOW_SECONDS")
    require_api_key: bool = Field(default=False, alias="REQUIRE_API_KEY")
    api_keys: list[str] = Field(default_factory=list, alias="API_KEYS")
    sql_dialect: str = Field(default="postgres", alias="SQL_DIALECT")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str]:
        """Accept comma-separated CORS origins from `.env`."""
        if value is None or value == "":
            return ["*"]
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return list(value)

    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, value: float) -> float:
        """Constrain model temperature to the OpenAI-compatible range."""
        if value < 0 or value > 2:
            raise ValueError("TEMPERATURE must be between 0 and 2")
        return value

    @field_validator("api_keys", mode="before")
    @classmethod
    def parse_api_keys(cls, value: Any) -> list[str]:
        if value is None or value == "":
            return []
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return list(value)


@lru_cache
def get_settings() -> Settings:
    """Load and cache settings."""
    load_dotenv()
    return Settings.model_validate(__import__("os").environ)
