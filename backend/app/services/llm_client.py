"""OpenAI-compatible LLM client."""

import asyncio
import re
from typing import Any

import httpx

from app.core.config import Settings
from app.core.exceptions import LLMUnavailableError, ValidationAppError
from app.services.prompt_builder import Prompt

FENCED_BLOCK_RE = re.compile(r"```(?:sql)?\s*(.*?)\s*```", re.IGNORECASE | re.DOTALL)


class LLMClient:
    """Reusable OpenAI-compatible chat completion client."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._timeout = httpx.Timeout(settings.request_timeout_seconds)

    async def generate_sql(self, prompt: Prompt) -> str:
        """Call the model and return normalized SQL text."""
        if not self._settings.openai_api_key:
            raise LLMUnavailableError("OPENAI_API_KEY is not configured")

        payload = {
            "model": self._settings.model_name,
            "messages": [
                {"role": "system", "content": prompt.system},
                {"role": "user", "content": prompt.user},
            ],
            "temperature": self._settings.temperature,
            "max_tokens": self._settings.max_tokens,
        }
        headers = {
            "Authorization": f"Bearer {self._settings.openai_api_key}",
            "Content-Type": "application/json",
        }

        last_error: Exception | None = None
        for attempt in range(self._settings.llm_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.post(
                        f"{self._settings.base_url.rstrip('/')}/chat/completions",
                        json=payload,
                        headers=headers,
                    )
                response.raise_for_status()
                return self._extract_sql(response.json())
            except (
                httpx.TimeoutException,
                httpx.HTTPError,
                KeyError,
                IndexError,
            ) as exc:
                last_error = exc
                if attempt >= self._settings.llm_retries:
                    break
                await asyncio.sleep(0.25 * (2**attempt))

        raise LLMUnavailableError() from last_error

    def _extract_sql(self, payload: dict[str, Any]) -> str:
        content = payload["choices"][0]["message"]["content"]
        if not isinstance(content, str) or not content.strip():
            raise ValidationAppError("LLM response did not contain SQL")
        return self.normalize_sql(content)

    @staticmethod
    def normalize_sql(value: str) -> str:
        """Strip markdown and normalize whitespace around SQL."""
        match = FENCED_BLOCK_RE.search(value)
        if match:
            value = match.group(1)
        value = value.strip().strip("`").strip()
        return re.sub(r"\s+", " ", value).strip()
