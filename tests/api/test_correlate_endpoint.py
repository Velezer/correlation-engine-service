from __future__ import annotations

import json
from pathlib import Path

from correlation_engine.api.routes import post_correlate

FIXTURES_DIR = Path("tests/fixtures")


def test_correlate_endpoint_returns_breakdown_and_rationale() -> None:
    payload = json.loads((FIXTURES_DIR / "couple_harmonious.json").read_text())

    response = post_correlate(payload)

    assert response["total_score"] == 72.2271
    assert len(response["contributions"]) == 5
    assert {item["rule"] for item in response["contributions"]} == {
        "sun_moon",
        "venus_mars",
        "major_aspects",
        "element_balance",
        "modality_balance",
    }
    assert "sun_moon=20.00/25.00" in response["rationale_text"]
    assert "generated_at_utc" in response


def test_correlate_endpoint_accepts_optional_weight_profile() -> None:
    payload = json.loads((FIXTURES_DIR / "couple_harmonious.json").read_text())
    payload["weight_profile"] = {
        "sun_moon": 10.0,
        "venus_mars": 10.0,
        "major_aspects": 10.0,
        "element_balance": 10.0,
        "modality_balance": 10.0,
    }

    response = post_correlate(payload)

    assert response["total_score"] == 39.2307
    assert response["contributions"][0]["weight"] == 10.0
