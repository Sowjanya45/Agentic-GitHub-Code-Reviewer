from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All configuration comes from environment variables (or a local .env)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"
    frontend_url: str = "http://localhost:5173"
    database_url: str = "postgresql+psycopg://codelens:codelens@localhost:5432/codelens"


@lru_cache
def get_settings() -> Settings:
    return Settings()
