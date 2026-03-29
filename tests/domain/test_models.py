from __future__ import annotations

from datetime import date, datetime, time

from correlation_engine.domain.models import (
    Aspect,
    AspectType,
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


def _fixture_chart() -> ComputedChart:
    return ComputedChart(
        planets=(
            PlanetPosition(planet=Planet.SUN, sign=ZodiacSign.ARIES, house=1, degree=10.5),
            PlanetPosition(planet=Planet.MOON, sign=ZodiacSign.CANCER, house=4, degree=2.25),
        ),
        signs=(
            SignPlacement(sign=ZodiacSign.ARIES, planet_count=1),
            SignPlacement(sign=ZodiacSign.CANCER, planet_count=1),
        ),
        houses=(
            HousePlacement(house=1, sign=ZodiacSign.ARIES),
            HousePlacement(house=4, sign=ZodiacSign.CANCER),
        ),
        aspects=(
            Aspect(
                planet_a=Planet.SUN,
                planet_b=Planet.MOON,
                aspect_type=AspectType.SQUARE,
                orb=1.75,
            ),
        ),
    )


def test_birth_input_accepts_concrete_values() -> None:
    birth = BirthInput(
        birth_date=date(1992, 7, 14),
        birth_time=time(9, 45),
        timezone="America/New_York",
        latitude=40.7128,
        longitude=-74.006,
    )

    assert birth.birth_date.isoformat() == "1992-07-14"
    assert birth.birth_time.isoformat() == "09:45:00"


def test_correlation_request_contract_with_real_chart_fixtures() -> None:
    chart_a = _fixture_chart()
    chart_b = _fixture_chart()
    request = CorrelationRequest(
        person_a_chart=chart_a,
        person_b_chart=chart_b,
        weighting_profile=WeightingProfile(
            planet_weight=0.4,
            sign_weight=0.2,
            house_weight=0.15,
            aspect_weight=0.25,
        ),
    )

    assert request.person_a_chart.planets[0].planet is Planet.SUN
    assert request.weighting_profile.aspect_weight == 0.25


def test_correlation_result_contract_payload() -> None:
    result = CorrelationResult(
        total_score=83.2,
        component_scores={
            "planets": 35.0,
            "signs": 20.0,
            "houses": 13.2,
            "aspects": 15.0,
        },
        explanation_payload={
            "highlights": ["Sun-Moon square drives tension"],
            "version": "v1",
        },
        generated_at_utc=datetime(2026, 3, 29, 12, 0, 0),
    )

    assert result.total_score == 83.2
    assert set(result.component_scores) == {"planets", "signs", "houses", "aspects"}
