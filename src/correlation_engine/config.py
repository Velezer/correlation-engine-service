"""Runtime configuration for the correlation engine service."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="CORRELATION_ENGINE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "correlation-engine-service"
    environment: str = Field(default="development", pattern=r"^(development|test|production)$")
    log_level: str = Field(default="INFO", pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings object for process-wide use."""

    return Settings()
