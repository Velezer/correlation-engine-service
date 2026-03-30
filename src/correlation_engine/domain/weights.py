"""Weight profiles for explainable correlation scoring."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CorrelationWeights(BaseModel):
    """Configurable weights for each scoring rule."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    sun_moon: float = Field(default=25.0, ge=0.0)
    venus_mars: float = Field(default=20.0, ge=0.0)
    major_aspects: float = Field(default=35.0, ge=0.0)
    element_balance: float = Field(default=10.0, ge=0.0)
    modality_balance: float = Field(default=10.0, ge=0.0)


DEFAULT_WEIGHTS = CorrelationWeights()
