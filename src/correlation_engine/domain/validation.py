"""Validation and normalization utilities for domain contracts."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import ValidationError

from correlation_engine.domain.models import BirthInput


class DomainValidationError(ValueError):
    """Raised when domain payloads fail validation."""


def validate_birth_input(payload: BirthInput | dict[str, object]) -> BirthInput:
    """Validate raw birth payload and return a typed, frozen model."""

    try:
        return payload if isinstance(payload, BirthInput) else BirthInput.model_validate(payload)
    except ValidationError as exc:
        raise DomainValidationError(f"Invalid birth input: {exc}") from exc


def birth_input_to_utc_datetime(birth_input: BirthInput) -> datetime:
    """Normalize a birth input to an aware UTC datetime."""

    try:
        source_timezone = ZoneInfo(birth_input.timezone)
    except ZoneInfoNotFoundError as exc:
        raise DomainValidationError(f"Unknown timezone: {birth_input.timezone}") from exc

    local_birth = datetime.combine(
        date=birth_input.birth_date,
        time=birth_input.birth_time,
        tzinfo=source_timezone,
    )
    return local_birth.astimezone(UTC)


def deterministic_serialize(value: object) -> str:
    """Serialize model/data structures deterministically for repeatable scoring."""

    normalized = value.model_dump(mode="json") if hasattr(value, "model_dump") else value
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
