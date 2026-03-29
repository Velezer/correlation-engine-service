"""Core astro-domain model declarations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


@dataclass(frozen=True, slots=True)
class AstroSignal:
    """A normalized astrological signal used for correlation evaluation."""

    source: str
    intensity: float


class Planet(StrEnum):
    """Supported planets/luminaries for chart computations."""

    SUN = "sun"
    MOON = "moon"
    MERCURY = "mercury"
    VENUS = "venus"
    MARS = "mars"
    JUPITER = "jupiter"
    SATURN = "saturn"
    URANUS = "uranus"
    NEPTUNE = "neptune"
    PLUTO = "pluto"


class ZodiacSign(StrEnum):
    """Supported zodiac signs."""

    ARIES = "aries"
    TAURUS = "taurus"
    GEMINI = "gemini"
    CANCER = "cancer"
    LEO = "leo"
    VIRGO = "virgo"
    LIBRA = "libra"
    SCORPIO = "scorpio"
    SAGITTARIUS = "sagittarius"
    CAPRICORN = "capricorn"
    AQUARIUS = "aquarius"
    PISCES = "pisces"


class AspectType(StrEnum):
    """Supported aspects for chart comparisons."""

    CONJUNCTION = "conjunction"
    OPPOSITION = "opposition"
    TRINE = "trine"
    SQUARE = "square"
    SEXTILE = "sextile"


class BirthInput(BaseModel):
    """Raw birth input needed to compute a natal chart."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    birth_date: date
    birth_time: time
    timezone: str = Field(min_length=1)
    latitude: float = Field(ge=-90.0, le=90.0)
    longitude: float = Field(ge=-180.0, le=180.0)


class PlanetPosition(BaseModel):
    """Computed planet location details in a chart."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    planet: Planet
    sign: ZodiacSign
    house: int = Field(ge=1, le=12)
    degree: float = Field(ge=0.0, lt=30.0)


class SignPlacement(BaseModel):
    """Computed sign-level aggregate for a chart."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    sign: ZodiacSign
    planet_count: int = Field(ge=0)


class HousePlacement(BaseModel):
    """Computed house-level aggregate for a chart."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    house: int = Field(ge=1, le=12)
    sign: ZodiacSign


class Aspect(BaseModel):
    """Computed aspect between two planets in a chart."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    planet_a: Planet
    planet_b: Planet
    aspect_type: AspectType
    orb: float = Field(ge=0.0, le=10.0)


class ComputedChart(BaseModel):
    """Fully computed chart entities used by correlation logic."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    planets: tuple[PlanetPosition, ...]
    signs: tuple[SignPlacement, ...]
    houses: tuple[HousePlacement, ...]
    aspects: tuple[Aspect, ...]


class WeightingProfile(BaseModel):
    """Weighting profile controls relative influence of score components."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    planet_weight: float = Field(ge=0.0)
    sign_weight: float = Field(ge=0.0)
    house_weight: float = Field(ge=0.0)
    aspect_weight: float = Field(ge=0.0)


class CorrelationRequest(BaseModel):
    """Input contract for a correlation computation."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    person_a_chart: ComputedChart
    person_b_chart: ComputedChart
    weighting_profile: WeightingProfile


class CorrelationResult(BaseModel):
    """Output contract for correlation scoring."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    total_score: float
    component_scores: dict[str, float]
    explanation_payload: dict[str, Any]
    generated_at_utc: datetime
