from __future__ import annotations

import logging.config
import os
from abc import ABC, abstractmethod
from typing import Optional

from dotenv import load_dotenv

from app.utils.secret_key import (
    create_google_secret_client,
    SecretKeyGoogleCloud,
    SecretKeyBase,
    MockSecretKey,
)
from app.utils.validators import DataBaseParameterValidator

load_dotenv()

logger = logging.getLogger(__name__)

DEVELOP_MODE: bool = os.getenv("DEVELOP_MODE", "True") == "True"


class DBSettingsBase(ABC):
    @property
    @abstractmethod
    def url(self) -> str:
        pass


class DatabaseSettings(DBSettingsBase):
    def __init__(
        self,
        database_scheme: str,
        secret: SecretKeyBase,
        validator_parameters: DataBaseParameterValidator,
    ) -> None:
        self.database_scheme = database_scheme
        self.secret = secret
        self.validator_parameters = validator_parameters

    @property
    def url(self) -> str:
        return (
            f"{self.database_scheme}://"
            f"{self._get_db_param('DB_USER')}:{self._get_db_param('DB_PASS')}"
            f"@{self._get_db_param('DB_HOST')}:{self._get_db_param('DB_PORT')}"
            f"/{self._get_db_param('DB_NAME')}"
        )

    async def _get_db_param(
        self, param: str, default: Optional[str] = None
    ) -> str:
        secret_value = await self.secret.get_secret_key(
            param, os.getenv(param, default)
        )

        return self.validator_parameters.validate_parameter_from_secret(
            param=param, value=secret_value
        )


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

secret_provider: SecretKeyBase

if DEVELOP_MODE:
    secret_provider = MockSecretKey()
else:
    secret_provider = SecretKeyGoogleCloud(
        client=create_google_secret_client()
    )

settings = Settings(
    db_settings=DatabaseSettings(
        database_scheme="postgresql+asyncpg",
        secret=secret_provider,
        validator_parameters=DataBaseParameterValidator(),
    )
)
