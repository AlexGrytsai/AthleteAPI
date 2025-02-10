import os
from typing import cast

from dotenv import load_dotenv

import app.core.logger_config  # noqa
from app.utils.secret_key import (
    create_google_secret_client,
    SecretKeyGoogleCloud,
    SecretKeyBase,
)

load_dotenv()

DEVELOP_MODE: bool = True


class Settings:
    def __init__(self, secret_key: SecretKeyBase):
        self.secret = secret_key

    @property
    def database_url(self):
        db_host: str = cast(
            str,
            self.secret.get_secret_key("DB_HOST", os.getenv("DB_HOST", "")),
        )
        db_port: int = cast(
            int,
            self.secret.get_secret_key("DB_PORT", os.getenv("DB_PORT", 5432)),
        )
        db_user: str = cast(
            str,
            self.secret.get_secret_key("DB_USER", os.getenv("DB_USER", "")),
        )
        db_pass: str = cast(
            str,
            self.secret.get_secret_key("DB_PASS", os.getenv("DB_PASS", "")),
        )
        db_name: str = cast(
            str,
            self.secret.get_secret_key("DB_NAME", os.getenv("DB_NAME", "")),
        )
        return (
            f"postgresql+asyncpg://"
            f"{db_user}:{db_pass}@{db_host}:{db_port}"
            f"/{db_name}"
        )


google_client = create_google_secret_client()

secret = SecretKeyGoogleCloud(client=google_client)

settings = Settings(secret_key=secret)
