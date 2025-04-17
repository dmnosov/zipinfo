import pytest
from pydantic import ValidationError

from infrastructure.adapters.sq.types import IssueStats


@pytest.mark.parametrize(
    ["total", "critical", "major", "minor"],
    [
        (50, 12, 13, 14),
        ("not-a-int", 5, 12, 31),
        (43, 13, 56, 7),
    ],
)
def test_validation(total: any, critical: int, major: int, minor: int):
    if isinstance(total, int):
        stats = IssueStats(total=total, critical=critical, major=major, minor=minor)

        assert stats.total == total
    else:
        with pytest.raises(ValidationError) as exc_info:
            IssueStats(total=total, critical=critical, major=major, minor=minor)

            assert "value is not a valid integer" in str(exc_info.value)
            assert exc_info.value.errors()[0]["loc"] == ("total",)
            assert exc_info.value.errors()[0]["type"] == "type_error.integer"
