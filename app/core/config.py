import logging.config

from pydantic_settings import BaseSettings

from app.utils.secret_key import secret


class Settings(BaseSettings):
    DB_HOST: str = secret.get_secret_key("DB_HOST", "localhost")
    DB_PORT: int = secret.get_secret_key("DB_PORT", 5432)
    DB_USER: str = secret.get_secret_key("DB_USER", "postgres")
    DB_PASS: str = secret.get_secret_key("DB_PASS", "postgres")
    DB_NAME: str = secret.get_secret_key("DB_NAME", "athlete_db")

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}"
            f"/{self.DB_NAME}"
        )


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "{levelname} [{asctime}] ({filename}) {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "main": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

settings = Settings()
