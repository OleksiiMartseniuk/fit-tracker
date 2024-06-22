from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    SQLALCHEMY_ECHO: bool = False
    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    # Admin settings
    ADMIN_SECRET_KEY: str
    # CORS
    CORS_ALLOWED_HOSTS: list[str]

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

    @property
    def postgres_async_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "": {  # root logger
            "level": "INFO",
            "handlers": ["default"],
            "propagate": False,
        },
        "uvicorn.error": {
            "level": "DEBUG",
            "handlers": ["default"],
        },
        "uvicorn.access": {
            "level": "DEBUG",
            "handlers": ["default"],
        },
    },
}
