from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    APP_NAME: str = "FinVerse AI"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = ""
    REDIS_URL: str = ""

    NEWS_API_KEY: str = ""
    ALPHA_VANTAGE_API_KEY: str = ""
    TWELVE_DATA_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    SECRET_KEY: str = ""

    CHROMADB_HOST: str = ""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env.development",
        extra="ignore"
    )


settings = Settings()