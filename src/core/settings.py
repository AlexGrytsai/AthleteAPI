from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "sqlite+aiosqlite:///./test.db"
