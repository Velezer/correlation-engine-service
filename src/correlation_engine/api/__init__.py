"""API entrypoints for service endpoints."""

from correlation_engine.api.health import health_status
from correlation_engine.api.routes import post_correlate

__all__ = ["health_status", "post_correlate"]
