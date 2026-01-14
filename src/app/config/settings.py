from pydantic_settings import BaseSettings
from pydantic import AnyUrl, Field


class Settings(BaseSettings):
    database_url: AnyUrl = Field(..., alias="DATABASE_URL")
    undo_token_secret: str = Field(..., alias="UNDO_TOKEN_SECRET")
    request_id_header: str = Field("X-Request-ID", alias="REQUEST_ID_HEADER")
    log_level: str = Field("INFO", alias="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


def get_settings() -> Settings:
    return Settings()  # type: ignore[arg-type]
