from dataclasses import dataclass

from fastapi.testclient import TestClient

from app.api.dependencies import get_query_service, get_rate_limiter
from app.core.config import get_settings
from app.main import app
from app.schemas.query import QuerySuccessResponse


@dataclass
class FakeQueryService:
    async def answer(self, question: str) -> QuerySuccessResponse:
        return QuerySuccessResponse(
            sql="SELECT 1 AS value",
            columns=["value"],
            rows=[{"value": 1}],
            rowCount=1,
            executionTime=0.001,
        )

    async def schema(self):
        from datetime import UTC, datetime

        from app.services.schema_loader import ColumnInfo, DatabaseSchema, TableInfo

        return DatabaseSchema(
            tables=[
                TableInfo(
                    name="employees",
                    columns=[
                        ColumnInfo(name="id", type="INTEGER", nullable=False),
                        ColumnInfo(name="name", type="TEXT", nullable=True),
                    ],
                    primary_keys=["id"],
                )
            ],
            loaded_at=datetime.now(UTC),
        )

    async def refresh_schema(self):
        return await self.schema()


def test_query_endpoint_success() -> None:
    app.dependency_overrides[get_query_service] = lambda: FakeQueryService()
    client = TestClient(app)

    response = client.post("/api/query", json={"question": "one"})

    assert response.status_code == 200
    assert response.json()["rowCount"] == 1
    app.dependency_overrides.clear()


def test_query_endpoint_validation_error() -> None:
    client = TestClient(app)

    response = client.post("/api/query", json={"question": ""})

    assert response.status_code == 400
    assert response.json()["success"] is False


def test_query_endpoint_requires_api_key(monkeypatch) -> None:
    monkeypatch.setenv("REQUIRE_API_KEY", "true")
    monkeypatch.setenv("API_KEYS", "secret-key")
    get_settings.cache_clear()
    get_rate_limiter.cache_clear()

    app.dependency_overrides[get_query_service] = lambda: FakeQueryService()
    client = TestClient(app)

    response = client.post("/api/query", json={"question": "one"})

    assert response.status_code == 401
    assert response.json()["success"] is False
    app.dependency_overrides.clear()


def test_query_endpoint_accepts_valid_api_key(monkeypatch) -> None:
    monkeypatch.setenv("REQUIRE_API_KEY", "true")
    monkeypatch.setenv("API_KEYS", "secret-key")
    get_settings.cache_clear()
    get_rate_limiter.cache_clear()

    app.dependency_overrides[get_query_service] = lambda: FakeQueryService()
    client = TestClient(app)

    response = client.post(
        "/api/query",
        json={"question": "one"},
        headers={"x-api-key": "secret-key"},
    )

    assert response.status_code == 200
    assert response.json()["rowCount"] == 1
    app.dependency_overrides.clear()


def test_query_endpoint_rate_limits(monkeypatch) -> None:
    monkeypatch.setenv("ENABLE_RATE_LIMITING", "true")
    monkeypatch.setenv("RATE_LIMIT_REQUESTS", "1")
    monkeypatch.setenv("RATE_LIMIT_WINDOW_SECONDS", "60")
    get_settings.cache_clear()
    get_rate_limiter.cache_clear()

    app.dependency_overrides[get_query_service] = lambda: FakeQueryService()
    client = TestClient(app)

    first = client.post("/api/query", json={"question": "one"})
    second = client.post("/api/query", json={"question": "two"})

    assert first.status_code == 200
    assert second.status_code == 429
    assert second.json()["success"] is False
    app.dependency_overrides.clear()


def test_query_logs_endpoint_returns_logs(monkeypatch) -> None:
    monkeypatch.setenv("REQUIRE_API_KEY", "true")
    monkeypatch.setenv("API_KEYS", "secret-key")
    get_settings.cache_clear()
    get_rate_limiter.cache_clear()

    app.dependency_overrides[get_query_service] = lambda: FakeQueryService()
    client = TestClient(app)

    client.post(
        "/api/query",
        json={"question": "one"},
        headers={"x-api-key": "secret-key"},
    )

    response = client.get(
        "/api/query/logs?limit=5",
        headers={"x-api-key": "secret-key"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["logs"]
    assert response.json()["logs"][0]["question"] == "one"
    app.dependency_overrides.clear()


def test_schema_endpoint_success() -> None:
    app.dependency_overrides[get_query_service] = lambda: FakeQueryService()
    client = TestClient(app)

    response = client.get("/api/schema")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["tables"][0]["name"] == "employees"
    assert body["tables"][0]["primaryKeys"] == ["id"]
    app.dependency_overrides.clear()
