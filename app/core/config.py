from __future__ import annotations

import asyncio
import logging.config
import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv

from app.utils.decorators import memory_profiler_class
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
PROFILER_MODE: bool = False


class DatabaseSettingsBase(ABC):
    @property
    @abstractmethod
    async def url(self) -> str:
        pass


@memory_profiler_class
class DatabaseSettings(DatabaseSettingsBase):
    __slots__ = ("_database_scheme", "_secret", "_validator_parameters")

    def __init__(
        self,
        database_scheme: str,
        secret: SecretKeyBase,
        validator_parameters: DataBaseParameterValidator,
    ) -> None:
        self._database_scheme = database_scheme
        self._secret = secret
        self._validator_parameters = validator_parameters

    @property
    async def url(self) -> str:
        db_user, db_pass, db_host, db_port, db_name = await asyncio.gather(
            self._get_db_param("DB_USER", default=os.getenv("DB_USER", "")),
            self._get_db_param("DB_PASS", default=os.getenv("DB_PASS", "")),
            self._get_db_param("DB_HOST", default=os.getenv("DB_HOST", "")),
            self._get_db_param("DB_PORT", default=os.getenv("DB_PORT", "")),
            self._get_db_param("DB_NAME", default=os.getenv("DB_NAME", "")),
        )

        return (
            f"{self._database_scheme}://"
            f"{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        )

    async def _get_db_param(self, param: str, default: str) -> str:
        secret_value = await self._secret.get_secret_key(param, default)

        return self._validator_parameters.validate_parameter_from_secret(
            param=param, value=secret_value
        )


@memory_profiler_class
class Settings:
    def __init__(self, db_settings: DatabaseSettingsBase) -> None:
        self._db_url = asyncio.run(db_settings.url)

    @property
    def database_url(self) -> str:
        return self._db_url


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
