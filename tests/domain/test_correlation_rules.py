from __future__ import annotations

import json
from pathlib import Path

from correlation_engine.domain.correlation import score_correlation
from correlation_engine.domain.models import ComputedChart
from correlation_engine.domain.weights import CorrelationWeights

FIXTURES_DIR = Path("tests/fixtures")


def _load_chart_pair(name: str) -> tuple[ComputedChart, ComputedChart]:
    payload = json.loads((FIXTURES_DIR / name).read_text())
    return (
        ComputedChart.model_validate(payload["profile_a"]),
        ComputedChart.model_validate(payload["profile_b"]),
    )


def _contrib_map(contributions: list[object]) -> dict[str, float]:
    return {item.rule: item.contribution for item in contributions}


def test_harmonious_pair_rule_subscores_are_stable() -> None:
    chart_a, chart_b = _load_chart_pair("couple_harmonious.json")

    total_score, contributions = score_correlation(chart_a, chart_b)

    by_rule = _contrib_map(contributions)
    assert total_score == 72.2271
    assert by_rule == {
        "sun_moon": 20.0,
        "venus_mars": 16.1071,
        "major_aspects": 18.12,
        "element_balance": 9.0,
        "modality_balance": 9.0,
    }


def test_challenging_pair_rule_subscores_are_stable() -> None:
    chart_a, chart_b = _load_chart_pair("couple_challenging.json")

    total_score, contributions = score_correlation(chart_a, chart_b)

    by_rule = _contrib_map(contributions)
    assert total_score == 59.8221
    assert by_rule == {
        "sun_moon": 18.125,
        "venus_mars": 8.8571,
        "major_aspects": 15.84,
        "element_balance": 8.0,
        "modality_balance": 9.0,
    }


def test_weight_profile_overrides_are_applied() -> None:
    chart_a, chart_b = _load_chart_pair("couple_harmonious.json")

    total_score, contributions = score_correlation(
        chart_a,
        chart_b,
        CorrelationWeights(
            sun_moon=50.0,
            venus_mars=0.0,
            major_aspects=25.0,
            element_balance=25.0,
            modality_balance=0.0,
        ),
    )

    by_rule = _contrib_map(contributions)
    assert by_rule["venus_mars"] == 0.0
    assert by_rule["modality_balance"] == 0.0
    assert total_score == 75.4429
