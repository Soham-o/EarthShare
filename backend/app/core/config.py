"""
Centralized, env-driven configuration.

Nothing in this codebase reads os.environ directly outside this module —
every setting flows through `Settings`, so there is one auditable place
that defines what configuration the app depends on, and a missing/invalid
value fails fast at startup instead of surfacing as a runtime bug later.
"""
from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- App ---
    app_name: str = "EarthShare API"
    environment: str = Field(default="development")  # development | production | test
    debug: bool = False

    # --- Database ---
    # Defaults to a local SQLite file so the project runs with zero external
    # setup. Point DATABASE_URL at a Postgres DSN for production deployments;
    # the rest of the stack (SQLAlchemy models, repositories) is unaffected.
    database_url: str = "sqlite:///./earthshare.db"

    # --- Auth / JWT ---
    # No insecure default is shipped for production: if ENVIRONMENT=production
    # and this is left at the placeholder, startup will refuse to boot.
    jwt_secret_key: str = "dev-only-insecure-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 12  # 12 hours

    # --- CORS ---
    cors_origins: str = "http://localhost:3000"
    # --- Rate limiting ---
    rate_limit_default: str = "100/minute"
    rate_limit_auth: str = "10/minute"

    # --- AI insights (optional) ---
    # If unset, the insight service transparently falls back to the local
    # rule-based generator. The app never depends on this being present.
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.0-flash"

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    if settings.is_production and settings.jwt_secret_key == "dev-only-insecure-secret-change-me":
        raise RuntimeError(
            "JWT_SECRET_KEY must be set to a strong, unique value when ENVIRONMENT=production."
        )
    return settings
