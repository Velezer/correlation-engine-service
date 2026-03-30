"""Rule-based synastry scoring with explainable contributions."""

from __future__ import annotations

from dataclasses import dataclass

from correlation_engine.domain.models import (
    AspectType,
    ComputedChart,
    Planet,
    PlanetPosition,
    ZodiacSign,
)
from correlation_engine.domain.weights import DEFAULT_WEIGHTS, CorrelationWeights

ELEMENT_BY_SIGN: dict[ZodiacSign, str] = {
    ZodiacSign.ARIES: "fire",
    ZodiacSign.LEO: "fire",
    ZodiacSign.SAGITTARIUS: "fire",
    ZodiacSign.TAURUS: "earth",
    ZodiacSign.VIRGO: "earth",
    ZodiacSign.CAPRICORN: "earth",
    ZodiacSign.GEMINI: "air",
    ZodiacSign.LIBRA: "air",
    ZodiacSign.AQUARIUS: "air",
    ZodiacSign.CANCER: "water",
    ZodiacSign.SCORPIO: "water",
    ZodiacSign.PISCES: "water",
}

MODALITY_BY_SIGN: dict[ZodiacSign, str] = {
    ZodiacSign.ARIES: "cardinal",
    ZodiacSign.CANCER: "cardinal",
    ZodiacSign.LIBRA: "cardinal",
    ZodiacSign.CAPRICORN: "cardinal",
    ZodiacSign.TAURUS: "fixed",
    ZodiacSign.LEO: "fixed",
    ZodiacSign.SCORPIO: "fixed",
    ZodiacSign.AQUARIUS: "fixed",
    ZodiacSign.GEMINI: "mutable",
    ZodiacSign.VIRGO: "mutable",
    ZodiacSign.SAGITTARIUS: "mutable",
    ZodiacSign.PISCES: "mutable",
}

COMPLEMENTARY_ELEMENTS: set[tuple[str, str]] = {
    ("fire", "air"),
    ("air", "fire"),
    ("water", "earth"),
    ("earth", "water"),
}

ASPECT_ANGLES: dict[AspectType, float] = {
    AspectType.CONJUNCTION: 0.0,
    AspectType.OPPOSITION: 180.0,
    AspectType.TRINE: 120.0,
    AspectType.SQUARE: 90.0,
    AspectType.SEXTILE: 60.0,
}

ASPECT_STRENGTH: dict[AspectType, float] = {
    AspectType.CONJUNCTION: 1.0,
    AspectType.TRINE: 0.9,
    AspectType.SEXTILE: 0.75,
    AspectType.OPPOSITION: 0.6,
    AspectType.SQUARE: 0.4,
}

SIGN_INDEX: dict[ZodiacSign, int] = {
    ZodiacSign.ARIES: 0,
    ZodiacSign.TAURUS: 1,
    ZodiacSign.GEMINI: 2,
    ZodiacSign.CANCER: 3,
    ZodiacSign.LEO: 4,
    ZodiacSign.VIRGO: 5,
    ZodiacSign.LIBRA: 6,
    ZodiacSign.SCORPIO: 7,
    ZodiacSign.SAGITTARIUS: 8,
    ZodiacSign.CAPRICORN: 9,
    ZodiacSign.AQUARIUS: 10,
    ZodiacSign.PISCES: 11,
}

PERSONAL_PLANETS: tuple[Planet, ...] = (
    Planet.SUN,
    Planet.MOON,
    Planet.MERCURY,
    Planet.VENUS,
    Planet.MARS,
)


@dataclass(frozen=True, slots=True)
class RuleContribution:
    """Single explainable rule contribution."""

    rule: str
    weight: float
    normalized_score: float
    contribution: float
    rationale: str


def _planet_map(chart: ComputedChart) -> dict[Planet, PlanetPosition]:
    return {position.planet: position for position in chart.planets}


def _sign_affinity(left: ZodiacSign, right: ZodiacSign) -> float:
    left_element = ELEMENT_BY_SIGN[left]
    right_element = ELEMENT_BY_SIGN[right]
    if left_element == right_element:
        return 1.0
    if (left_element, right_element) in COMPLEMENTARY_ELEMENTS:
        return 0.85
    if MODALITY_BY_SIGN[left] == MODALITY_BY_SIGN[right]:
        return 0.6
    return 0.35


def _longitude(position: PlanetPosition) -> float:
    return SIGN_INDEX[position.sign] * 30.0 + position.degree


def _closest_aspect_strength(
    left: PlanetPosition,
    right: PlanetPosition,
    orb_limit: float = 6.0,
) -> float:
    separation = abs(_longitude(left) - _longitude(right))
    distance = min(separation, 360.0 - separation)
    strengths: list[float] = []
    for aspect, angle in ASPECT_ANGLES.items():
        orb = abs(distance - angle)
        if orb <= orb_limit:
            strengths.append(ASPECT_STRENGTH[aspect] * (1.0 - (orb / (orb_limit + 1.0))))
    return max(strengths, default=0.5)


def _distribution_similarity(values_a: list[str], values_b: list[str]) -> float:
    keys = sorted(set(values_a + values_b))
    counts_a = {key: values_a.count(key) / len(values_a) for key in keys}
    counts_b = {key: values_b.count(key) / len(values_b) for key in keys}
    l1_distance = sum(abs(counts_a[key] - counts_b[key]) for key in keys)
    similarity = 1.0 - (l1_distance / 2.0)
    return max(0.0, min(1.0, similarity))


def score_correlation(
    chart_a: ComputedChart,
    chart_b: ComputedChart,
    weights: CorrelationWeights = DEFAULT_WEIGHTS,
) -> tuple[float, list[RuleContribution]]:
    """Score synastry correlation and return weighted, explainable rule contributions."""

    planets_a = _planet_map(chart_a)
    planets_b = _planet_map(chart_b)

    sun_moon_score = (
        _sign_affinity(planets_a[Planet.SUN].sign, planets_b[Planet.MOON].sign)
        + _sign_affinity(planets_b[Planet.SUN].sign, planets_a[Planet.MOON].sign)
    ) / 2.0

    venus_mars_score = (
        _sign_affinity(planets_a[Planet.VENUS].sign, planets_b[Planet.MARS].sign)
        + _sign_affinity(planets_b[Planet.VENUS].sign, planets_a[Planet.MARS].sign)
        + _closest_aspect_strength(planets_a[Planet.VENUS], planets_b[Planet.MARS])
        + _closest_aspect_strength(planets_b[Planet.VENUS], planets_a[Planet.MARS])
    ) / 4.0

    aspect_scores = [
        _closest_aspect_strength(planets_a[left], planets_b[right])
        for left in PERSONAL_PLANETS
        for right in PERSONAL_PLANETS
    ]
    major_aspects_score = sum(aspect_scores) / len(aspect_scores)

    element_balance_score = _distribution_similarity(
        [ELEMENT_BY_SIGN[p.sign] for p in chart_a.planets],
        [ELEMENT_BY_SIGN[p.sign] for p in chart_b.planets],
    )
    modality_balance_score = _distribution_similarity(
        [MODALITY_BY_SIGN[p.sign] for p in chart_a.planets],
        [MODALITY_BY_SIGN[p.sign] for p in chart_b.planets],
    )

    raw_rules: list[tuple[str, float, float, str]] = [
        (
            "sun_moon",
            weights.sun_moon,
            sun_moon_score,
            "Sun/Moon cross-pair emotional resonance.",
        ),
        (
            "venus_mars",
            weights.venus_mars,
            venus_mars_score,
            "Venus/Mars attraction via sign chemistry and cross-aspects.",
        ),
        (
            "major_aspects",
            weights.major_aspects,
            major_aspects_score,
            "Average major aspect harmony across personal planets.",
        ),
        (
            "element_balance",
            weights.element_balance,
            element_balance_score,
            "Element distribution similarity across both charts.",
        ),
        (
            "modality_balance",
            weights.modality_balance,
            modality_balance_score,
            "Modality distribution similarity across both charts.",
        ),
    ]

    contributions = [
        RuleContribution(
            rule=rule,
            weight=weight,
            normalized_score=round(normalized, 4),
            contribution=round(weight * normalized, 4),
            rationale=rationale,
        )
        for rule, weight, normalized, rationale in raw_rules
    ]
    total_score = round(sum(item.contribution for item in contributions), 4)
    return total_score, contributions
