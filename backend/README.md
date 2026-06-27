# AI Text-to-SQL Backend

Production-oriented FastAPI backend for generating, validating, and executing safe read-only SQL from natural language.

## Features

- `POST /api/query` Text-to-SQL pipeline
- Async SQLAlchemy 2.x database access
- PostgreSQL first, SQLite supported for development
- OpenAI-compatible chat completions client
- Cached schema introspection with tables, columns, primary keys, and foreign keys
- Mandatory SQL validation with `sqlglot`
- Read-only execution transactions
- Structured JSON logs with request ids
- Persisted query audit logging with request id and client key
- Consistent safe error responses
- Pytest coverage for API, validator, parser behavior, executor, prompt builder, LLM client, schema loader, and query logger

## Quick Start

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

The app starts without a configured key, but `/api/query` returns `503` until `OPENAI_API_KEY` is set.

## Configuration

All runtime configuration is read from `.env` or environment variables:

```env
OPENAI_API_KEY=
DATABASE_URL=sqlite+aiosqlite:///./text_to_sql.db
MODEL_NAME=gpt-4.1-mini
BASE_URL=https://api.openai.com/v1
APP_ENV=development
LOG_LEVEL=INFO
TEMPERATURE=0
MAX_TOKENS=512
REQUEST_TIMEOUT_SECONDS=30
LLM_RETRIES=2
CORS_ORIGINS=*
MAX_QUESTION_LENGTH=2000
MAX_REQUEST_BYTES=16384
SCHEMA_CACHE_TTL_SECONDS=300
ENABLE_RATE_LIMITING=false
RATE_LIMIT_REQUESTS=60
RATE_LIMIT_WINDOW_SECONDS=60
REQUIRE_API_KEY=false
API_KEYS=
SQL_DIALECT=postgres
```

For PostgreSQL async connections, use:

```env
DATABASE_URL=postgresql+asyncpg://text_to_sql:text_to_sql@localhost:5432/text_to_sql
SQL_DIALECT=postgres
```

## API

The frontend uses Vite's development proxy to call these endpoints through `/api/*`.

### `POST /api/query`

Request:

```json
{
  "question": "Show all employees earning above 50000"
}
```

Success:

```json
{
  "success": true,
  "sql": "SELECT ...",
  "columns": [],
  "rows": [],
  "rowCount": 10,
  "executionTime": 0.18
}
```

Error:

```json
{
  "success": false,
  "error": {
    "type": "UNSAFE_SQL",
    "message": "Only SELECT statements are allowed"
  }
}
```

## Pipeline

`Request -> Validation -> Cached Schema -> Prompt -> LLM -> SQL Extraction -> SQL Validation -> Read-only Execution -> Response`

Each stage lives in its own module under `app/services` and is independently testable.

## Docker

```bash
copy .env.example .env
docker compose up --build
```

When using Compose, set:

```env
DATABASE_URL=postgresql+asyncpg://text_to_sql:text_to_sql@postgres:5432/text_to_sql
```

## Tests

```bash
pytest
```

## Security Notes

- Generated SQL is parsed and validated before execution.
- Only one `SELECT` statement is allowed.
- Comments, multiple statements, stored procedure calls, DDL, and DML are rejected.
- Database work runs inside a transaction that is rolled back.
- PostgreSQL uses `SET TRANSACTION READ ONLY`; SQLite enables `PRAGMA query_only`.
- Public errors never include stack traces or credentials.
