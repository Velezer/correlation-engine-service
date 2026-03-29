"""Structured logging bootstrap for the correlation engine service."""

from __future__ import annotations

import logging
from typing import cast

import structlog


def configure_logging(level: str = "INFO") -> None:
    """Configure stdlib + structlog formatters once at process startup."""

    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO), format="%(message)s")
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Return a structured logger instance for modules to use."""

    return cast(structlog.stdlib.BoundLogger, structlog.get_logger(name))
