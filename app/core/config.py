from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "RepoLens AI"
    database_url: str

    github_api_base_url: str = "https://api.github.com"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()