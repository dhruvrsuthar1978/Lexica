import httpx
import pytest

from app.core.config import Settings
from app.services.llm_client import LLMClient
from app.services.prompt_builder import Prompt


def test_normalize_sql_strips_markdown() -> None:
    sql = LLMClient.normalize_sql("```sql\nSELECT *\nFROM employees\n```")
    assert sql == "SELECT * FROM employees"


@pytest.mark.asyncio
async def test_generate_sql_parses_openai_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = Settings.model_validate(
        {
            "OPENAI_API_KEY": "test-key",
            "DATABASE_URL": "sqlite+aiosqlite:///:memory:",
            "MODEL_NAME": "test-model",
            "BASE_URL": "https://example.test/v1",
            "APP_ENV": "test",
            "LOG_LEVEL": "INFO",
            "TEMPERATURE": "0",
            "MAX_TOKENS": "64",
        }
    )

    async def fake_post(
        self: httpx.AsyncClient, *args: object, **kwargs: object
    ) -> httpx.Response:
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": "SELECT id FROM employees"}}]},
            request=httpx.Request("POST", "https://example.test/v1/chat/completions"),
        )

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)

    sql = await LLMClient(settings).generate_sql(Prompt(system="sys", user="user"))

    assert sql == "SELECT id FROM employees"
