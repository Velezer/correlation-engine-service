"""Baseline tests validating scaffold behavior."""

from correlation_engine.api import health_status
from correlation_engine.domain import AstroSignal, CorrelationRule, evaluate_correlation


def test_health_status_ok() -> None:
    response = health_status()

    assert response["status"] == "ok"


def test_evaluate_correlation_threshold() -> None:
    signal = AstroSignal(source="moon_phase", intensity=0.8)
    rule = CorrelationRule(name="high-signal", threshold=0.5)

    assert evaluate_correlation(signal=signal, rule=rule)
