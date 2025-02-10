import logging.config
import os
from abc import ABC, abstractmethod
from typing import cast, Union, Optional

from dotenv import load_dotenv

from app.utils.secret_key import (
    create_google_secret_client,
    SecretKeyGoogleCloud,
    SecretKeyBase,
)

load_dotenv()

logger = logging.getLogger(__name__)

DEVELOP_MODE: bool = True


class DBSettingsBase(ABC):
    @abstractmethod
    def url(self) -> str:
        pass


class DatabaseSettings(DBSettingsBase):
    def __init__(self, database_scheme: str, secret: SecretKeyBase) -> None:
        self.database_scheme = database_scheme
        self.secret = secret

    @property
    def url(self) -> str:
        return (
            f"{self.database_scheme}://"
            f"{self._get_db_param('DB_USER')}:{self._get_db_param('DB_PASS')}"
            f"@{self._get_db_param('DB_HOST')}:{self._get_db_param('DB_PORT')}"
            f"/{self._get_db_param('DB_NAME')}"
        )

    def _get_db_param(
        self, param: str, default: Optional[Union[str, int]] = None
    ) -> Union[str, int]:
        secret_value = self.secret.get_secret_key(
            param, os.getenv(param, default)
        )

        return self._validate_param_type(param=param, value=secret_value)

    @staticmethod
    def _validate_param_type(
        param: str,
        value: Union[str, int, None],
    ) -> Union[str, int]:
        if isinstance(value, (str, int)):
            if param == "DB_HOST" and isinstance(value, int):
                return value
            return value

        error_message = (
            f"Invalid type for database parameter '{param}'. "
            f"Value '{value}' has type '{type(value).__name__}'. "
            f"Allowed types: int or str."
        )
        logger.error(error_message)
        raise TypeError(error_message)


class Settings:
    def __init__(self, db_settings: DBSettingsBase):
        self.db_url = db_settings.url


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

settings = Settings(
    db_settings=DatabaseSettings(
        database_scheme="postgresql+asyncpg",
        secret=SecretKeyGoogleCloud(client=create_google_secret_client()),
    )
)
