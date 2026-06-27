from datetime import UTC, datetime

from app.services.prompt_builder import PromptBuilder
from app.services.schema_loader import ColumnInfo, DatabaseSchema, TableInfo


def test_prompt_contains_schema_and_rules() -> None:
    schema = DatabaseSchema(
        tables=[
            TableInfo(
                name="employees",
                columns=[ColumnInfo(name="id", type="INTEGER", nullable=False)],
                primary_keys=["id"],
            )
        ],
        loaded_at=datetime.now(UTC),
    )

    prompt = PromptBuilder("postgres").build("Show employees", schema)

    assert "Only SELECT queries." in prompt.system
    assert "Table: employees" in prompt.system
    assert "Question: Show employees" == prompt.user
