from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "sqlite+aiosqlite:///./test_db.sqlite3"
    # DB_ECHO: bool = False
    DB_ECHO: bool = True


settings = Settings()
