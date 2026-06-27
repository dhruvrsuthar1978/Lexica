"""Prompt construction for Text-to-SQL generation."""

from dataclasses import dataclass

from app.services.schema_loader import DatabaseSchema


@dataclass(frozen=True)
class Prompt:
    """Messages sent to an OpenAI-compatible chat completion API."""

    system: str
    user: str


class PromptBuilder:
    """Builds strict prompts for SQL generation."""

    def __init__(self, dialect: str) -> None:
        self._dialect = dialect

    def build(self, question: str, schema: DatabaseSchema) -> Prompt:
        """Create system and user messages for the LLM."""
        system = f"""You are an expert SQL generator.
Generate SQL only.
No markdown.
No explanations.
No comments.
No code fences.
Only one SQL statement.
Only SELECT queries.
Use the {self._dialect} SQL dialect.
Use only tables and columns present in the schema.
Prefer explicit joins using the relationship information.

Database schema:
{schema.to_prompt_text()}
"""
        user = f"Question: {question}"
        return Prompt(system=system.strip(), user=user)
