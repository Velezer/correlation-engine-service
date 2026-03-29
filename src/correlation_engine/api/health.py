"""Basic service endpoint handlers."""

from typing import TypedDict


class HealthResponse(TypedDict):
    """Shape returned by health endpoint."""

    status: str


def health_status() -> HealthResponse:
    """Return service health payload."""

    return {"status": "ok"}
