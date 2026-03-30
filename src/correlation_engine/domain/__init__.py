"""Domain entities and rule primitives."""

from correlation_engine.domain.correlation import RuleContribution, score_correlation
from correlation_engine.domain.models import (
    Aspect,
    AspectType,
    AstroSignal,
    BirthInput,
    ComputedChart,
    CorrelationRequest,
    CorrelationResult,
    HousePlacement,
    Planet,
    PlanetPosition,
    SignPlacement,
    WeightingProfile,
    ZodiacSign,
)
from correlation_engine.domain.rules import CorrelationRule, evaluate_correlation
from correlation_engine.domain.validation import (
    DomainValidationError,
    birth_input_to_utc_datetime,
    deterministic_serialize,
    validate_birth_input,
)
from correlation_engine.domain.weights import CorrelationWeights

__all__ = [
    "Aspect",
    "AspectType",
    "AstroSignal",
    "BirthInput",
    "ComputedChart",
    "CorrelationRequest",
    "CorrelationResult",
    "CorrelationRule",
    "CorrelationWeights",
    "DomainValidationError",
    "HousePlacement",
    "Planet",
    "PlanetPosition",
    "RuleContribution",
    "SignPlacement",
    "WeightingProfile",
    "ZodiacSign",
    "birth_input_to_utc_datetime",
    "deterministic_serialize",
    "evaluate_correlation",
    "score_correlation",
    "validate_birth_input",
]
