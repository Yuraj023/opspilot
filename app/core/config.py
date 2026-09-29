from functools import lru_cache

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    app_name: str = "OpsPilot"

    api_prefix: str = "/api/v1"

    database_url: str = "sqlite:///./opspilot.db"

    openrouter_api_key: str | None = Field(
        default=None,
        alias="OPENROUTER_API_KEY",
    )

    llm_base_url: str = (
        "https://openrouter.ai/api/v1"
    )

    llm_model: str = "openai/gpt-5-mini"

    disable_sdk_tracing: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()