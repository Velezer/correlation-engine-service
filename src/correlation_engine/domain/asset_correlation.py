"""Market-asset correlation utilities."""

from __future__ import annotations

from itertools import combinations
from math import sqrt

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AssetSeries(BaseModel):
    """Price series for a single asset symbol."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    symbol: str = Field(min_length=1)
    prices: tuple[float, ...] = Field(min_length=2)


class AssetCorrelationRequest(BaseModel):
    """Request model for multi-asset Pearson correlation."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    assets: tuple[AssetSeries, ...] = Field(min_length=2)

    @model_validator(mode="after")
    def validate_distinct_symbols_and_length(self) -> AssetCorrelationRequest:
        symbols = [asset.symbol.upper() for asset in self.assets]
        if len(set(symbols)) != len(symbols):
            msg = "Asset symbols must be unique."
            raise ValueError(msg)

        length_set = {len(asset.prices) for asset in self.assets}
        if len(length_set) != 1:
            msg = "All assets must contain the same number of prices."
            raise ValueError(msg)

        return self


def _pearson(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    sample_size = len(left)
    mean_left = sum(left) / sample_size
    mean_right = sum(right) / sample_size

    numerator = sum((x - mean_left) * (y - mean_right) for x, y in zip(left, right, strict=True))
    denominator_left = sum((x - mean_left) ** 2 for x in left)
    denominator_right = sum((y - mean_right) ** 2 for y in right)
    denominator = sqrt(denominator_left * denominator_right)

    if denominator == 0.0:
        return 0.0

    return round(numerator / denominator, 6)


def build_correlation_matrix(request: AssetCorrelationRequest) -> dict[str, dict[str, float]]:
    """Build a symmetric Pearson correlation matrix keyed by symbol."""

    symbols = [asset.symbol.upper() for asset in request.assets]
    prices_by_symbol = {asset.symbol.upper(): asset.prices for asset in request.assets}

    matrix: dict[str, dict[str, float]] = {
        symbol: {inner: 1.0 if symbol == inner else 0.0 for inner in symbols} for symbol in symbols
    }

    for left_symbol, right_symbol in combinations(symbols, 2):
        value = _pearson(prices_by_symbol[left_symbol], prices_by_symbol[right_symbol])
        matrix[left_symbol][right_symbol] = value
        matrix[right_symbol][left_symbol] = value

    return matrix
