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
