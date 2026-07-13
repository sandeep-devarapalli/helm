from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="HELM_",
        extra="ignore",
    )

    environment: str = "development"
    hermes_version: str = "not-configured"
    vibe_version: str = "not-configured"
    database_url: SecretStr = SecretStr(
        "postgresql+asyncpg://helm:helm@postgres:5432/helm"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
