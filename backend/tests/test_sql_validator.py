import pytest

from app.core.exceptions import UnsafeSQLError
from app.services.sql_validator import SQLValidator


@pytest.fixture
def validator() -> SQLValidator:
    return SQLValidator("postgres")


def test_accepts_select(validator: SQLValidator) -> None:
    assert validator.validate("select id, name from employees").startswith("SELECT")


@pytest.mark.parametrize(
    "sql",
    [
        "update employees set salary = 1",
        "delete from employees",
        "drop table employees",
        "select * from employees; select * from departments",
        "select * from employees -- nope",
        "call dangerous_proc()",
        "vacuum",
    ],
)
def test_rejects_unsafe_sql(validator: SQLValidator, sql: str) -> None:
    with pytest.raises(UnsafeSQLError):
        validator.validate(sql)
