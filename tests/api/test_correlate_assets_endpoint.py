from __future__ import annotations

from correlation_engine.api.routes import post_correlate_assets


def test_correlate_assets_endpoint_returns_matrix() -> None:
    payload = {
        "assets": [
            {"symbol": "BTC", "prices": [100.0, 102.0, 101.0, 105.0, 110.0]},
            {"symbol": "gold", "prices": [1900.0, 1905.0, 1903.0, 1908.0, 1915.0]},
            {"symbol": "LINK", "prices": [7.0, 7.4, 7.2, 7.9, 8.4]},
        ]
    }

    response = post_correlate_assets(payload)

    assert response["symbols"] == ["BTC", "GOLD", "LINK"]
    assert response["correlation_matrix"]["BTC"]["GOLD"] == 0.989734
    assert response["correlation_matrix"]["BTC"]["LINK"] == 0.988659
    assert response["correlation_matrix"]["GOLD"]["LINK"] == 0.987703
    assert "generated_at_utc" in response
