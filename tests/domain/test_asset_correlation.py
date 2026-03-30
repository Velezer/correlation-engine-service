from __future__ import annotations

import pytest
from pydantic import ValidationError

from correlation_engine.domain.asset_correlation import (
    AssetCorrelationRequest,
    build_correlation_matrix,
)


def test_build_correlation_matrix_for_btc_gold_link() -> None:
    request = AssetCorrelationRequest.model_validate(
        {
            "assets": [
                {"symbol": "BTC", "prices": [100.0, 102.0, 101.0, 105.0, 110.0]},
                {"symbol": "GOLD", "prices": [1900.0, 1905.0, 1903.0, 1908.0, 1915.0]},
                {"symbol": "LINK", "prices": [7.0, 7.4, 7.2, 7.9, 8.4]},
            ]
        }
    )

    matrix = build_correlation_matrix(request)

    assert matrix["BTC"]["BTC"] == 1.0
    assert matrix["GOLD"]["GOLD"] == 1.0
    assert matrix["LINK"]["LINK"] == 1.0
    assert matrix["BTC"]["GOLD"] == 0.989734
    assert matrix["BTC"]["LINK"] == 0.988659
    assert matrix["GOLD"]["LINK"] == 0.987703


def test_asset_correlation_rejects_duplicate_symbols() -> None:
    with pytest.raises(ValidationError):
        AssetCorrelationRequest.model_validate(
            {
                "assets": [
                    {"symbol": "BTC", "prices": [1.0, 2.0, 3.0]},
                    {"symbol": "btc", "prices": [1.1, 2.1, 3.1]},
                ]
            }
        )


def test_asset_correlation_rejects_mismatched_price_lengths() -> None:
    with pytest.raises(ValidationError):
        AssetCorrelationRequest.model_validate(
            {
                "assets": [
                    {"symbol": "BTC", "prices": [1.0, 2.0, 3.0]},
                    {"symbol": "GOLD", "prices": [1.0, 2.0]},
                ]
            }
        )
