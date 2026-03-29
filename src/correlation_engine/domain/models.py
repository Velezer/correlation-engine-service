"""Core astro-domain model declarations."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AstroSignal:
    """A normalized astrological signal used for correlation evaluation."""

    source: str
    intensity: float
