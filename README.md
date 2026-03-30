# Correlation Engine Service

A typed Python service scaffold for astro model correlations.

## Prerequisites

- Python 3.12+
- `pip`

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

## Run checks locally

```bash
ruff check .
ruff format --check .
mypy src tests
pyright
pytest
```

## Pre-commit

```bash
pre-commit install
pre-commit run --all-files
```

## Configuration

Runtime settings read environment variables prefixed with `CORRELATION_ENGINE_`.

Example:

```bash
export CORRELATION_ENGINE_ENVIRONMENT=production
export CORRELATION_ENGINE_LOG_LEVEL=INFO
```

## CI

CI runs linting, typing, and tests on every push and pull request via GitHub Actions.

## Correlating market assets (BTC, GOLD, LINK)

You can use the framework-agnostic `post_correlate_assets` endpoint helper with explicit
price series. Each asset must provide the same number of price points.

```python
from correlation_engine.api.routes import post_correlate_assets

payload = {
    "assets": [
        {"symbol": "BTC", "prices": [100.0, 102.0, 101.0, 105.0, 110.0]},
        {"symbol": "GOLD", "prices": [1900.0, 1905.0, 1903.0, 1908.0, 1915.0]},
        {"symbol": "LINK", "prices": [7.0, 7.4, 7.2, 7.9, 8.4]},
    ]
}

response = post_correlate_assets(payload)
print(response["correlation_matrix"])
```
