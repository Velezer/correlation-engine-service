"""Correlation rules and evaluators for astro signals."""

from dataclasses import dataclass

from correlation_engine.domain.models import AstroSignal


@dataclass(frozen=True, slots=True)
class CorrelationRule:
    """Threshold rule to classify a signal as correlated."""

    name: str
    threshold: float


def evaluate_correlation(signal: AstroSignal, rule: CorrelationRule) -> bool:
    """Evaluate whether a signal satisfies the given correlation rule."""

    return signal.intensity >= rule.threshold
