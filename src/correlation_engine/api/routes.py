"""API routes for correlation requests."""

from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from correlation_engine.domain.correlation import score_correlation
from correlation_engine.domain.models import ComputedChart
from correlation_engine.domain.weights import CorrelationWeights


class CorrelateRequest(BaseModel):
    """Request payload for correlation endpoint."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    profile_a: ComputedChart
    profile_b: ComputedChart
    weight_profile: CorrelationWeights | None = None


class CorrelateResponse(BaseModel):
    """Structured response payload for correlation endpoint."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    total_score: float
    contributions: list[dict[str, Any]]
    rationale_text: str
    generated_at_utc: datetime


def post_correlate(payload: dict[str, Any]) -> dict[str, Any]:
    """Handle a correlate request in a framework-agnostic endpoint function."""

    request = CorrelateRequest.model_validate(payload)
    weights = request.weight_profile or CorrelationWeights()
    total_score, contributions = score_correlation(request.profile_a, request.profile_b, weights)

    rationale_text = "; ".join(
        f"{item.rule}={item.contribution:.2f}/{item.weight:.2f}" for item in contributions
    )

    response = CorrelateResponse(
        total_score=total_score,
        contributions=[asdict(item) for item in contributions],
        rationale_text=rationale_text,
        generated_at_utc=datetime.now(tz=UTC),
    )
    return response.model_dump(mode="json")
