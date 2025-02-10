import os
from typing import cast

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

import app.core.logger_config  # noqa
from app.utils.secret_key import secret

load_dotenv()


class Settings(BaseSettings):
    DEVELOP_MODE: bool = True

    DB_HOST: str = cast(
        str, secret.get_secret_key("DB_HOST", os.getenv("DB_HOST", ""))
    )
    DB_PORT: int = cast(
        int, secret.get_secret_key("DB_PORT", os.getenv("DB_PORT", 5432))
    )
    DB_USER: str = cast(
        str, secret.get_secret_key("DB_USER", os.getenv("DB_USER", ""))
    )
    DB_PASS: str = cast(
        str, secret.get_secret_key("DB_PASS", os.getenv("DB_PASS", ""))
    )
    DB_NAME: str = cast(
        str, secret.get_secret_key("DB_NAME", os.getenv("DB_NAME", ""))
    )

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}"
            f"/{self.DB_NAME}"
        )


settings = Settings()
