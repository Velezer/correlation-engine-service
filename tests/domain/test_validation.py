from __future__ import annotations

from datetime import UTC, date, datetime, time

import pytest

from correlation_engine.domain.models import BirthInput
from correlation_engine.domain.validation import (
    DomainValidationError,
    birth_input_to_utc_datetime,
    deterministic_serialize,
    validate_birth_input,
)


def test_validate_birth_input_rejects_impossible_date() -> None:
    with pytest.raises(DomainValidationError):
        validate_birth_input(
            {
                "birth_date": "2025-02-30",
                "birth_time": "12:10:00",
                "timezone": "UTC",
                "latitude": 10.0,
                "longitude": 10.0,
            }
        )


def test_validate_birth_input_rejects_impossible_time() -> None:
    with pytest.raises(DomainValidationError):
        validate_birth_input(
            {
                "birth_date": "2025-02-28",
                "birth_time": "24:00:00",
                "timezone": "UTC",
                "latitude": 10.0,
                "longitude": 10.0,
            }
        )


def test_validate_birth_input_rejects_out_of_range_coordinates() -> None:
    with pytest.raises(DomainValidationError):
        validate_birth_input(
            {
                "birth_date": "2025-02-28",
                "birth_time": "23:59:00",
                "timezone": "UTC",
                "latitude": 92.0,
                "longitude": -181.0,
            }
        )


def test_birth_input_to_utc_datetime_normalizes_timezone() -> None:
    birth = BirthInput(
        birth_date=date(2024, 1, 1),
        birth_time=time(0, 30),
        timezone="America/Los_Angeles",
        latitude=34.0522,
        longitude=-118.2437,
    )

    actual_utc = birth_input_to_utc_datetime(birth)

    assert actual_utc == datetime(2024, 1, 1, 8, 30, tzinfo=UTC)


def test_deterministic_serialize_produces_repeatable_output() -> None:
    left = {
        "b": 2,
        "a": 1,
        "nested": {"y": 9, "x": 8},
    }
    right = {
        "nested": {"x": 8, "y": 9},
        "a": 1,
        "b": 2,
    }

    assert deterministic_serialize(left) == deterministic_serialize(right)
    assert deterministic_serialize(left) == '{"a":1,"b":2,"nested":{"x":8,"y":9}}'
