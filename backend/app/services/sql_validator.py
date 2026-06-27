"""SQL safety validation."""

import re

import sqlglot
from sqlglot import exp

from app.core.exceptions import UnsafeSQLError

COMMENT_RE = re.compile(r"(--|/\*|\*/)")
FORBIDDEN_EXPRESSIONS: tuple[type[exp.Expression], ...] = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Drop,
    exp.Alter,
    exp.Create,
    exp.Merge,
    exp.Command,
    exp.Grant,
)
FORBIDDEN_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "MERGE",
    "CALL",
    "EXEC",
    "EXECUTE",
    "GRANT",
    "REVOKE",
    "COPY",
    "VACUUM",
}


class SQLValidator:
    """Validates that generated SQL is a single safe SELECT statement."""

    def __init__(self, dialect: str) -> None:
        self._dialect = dialect

    def validate(self, sql: str) -> str:
        """Return normalized SQL if safe, otherwise raise UnsafeSQLError."""
        normalized = sql.strip()
        if not normalized:
            raise UnsafeSQLError("Generated SQL is empty")
        if COMMENT_RE.search(normalized):
            raise UnsafeSQLError("SQL comments are not allowed")
        if self._has_forbidden_keyword(normalized):
            raise UnsafeSQLError("Only SELECT statements are allowed")

        try:
            expressions = sqlglot.parse(normalized, read=self._dialect)
        except sqlglot.errors.ParseError as exc:
            raise UnsafeSQLError("Generated SQL could not be parsed") from exc

        if len(expressions) != 1:
            raise UnsafeSQLError("Only one SQL statement is allowed")

        expression = expressions[0]
        if not isinstance(expression, exp.Select):
            raise UnsafeSQLError("Only SELECT statements are allowed")
        if any(isinstance(node, FORBIDDEN_EXPRESSIONS) for node in expression.walk()):
            raise UnsafeSQLError("Unsafe SQL operation is not allowed")

        return expression.sql(dialect=self._dialect)

    @staticmethod
    def _has_forbidden_keyword(sql: str) -> bool:
        tokens = {token.upper() for token in re.findall(r"\b[A-Za-z_]+\b", sql)}
        return bool(tokens & FORBIDDEN_KEYWORDS)
