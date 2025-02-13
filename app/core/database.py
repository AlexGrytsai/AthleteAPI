from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)

from app.core.config import settings


def create_database_engine(database_url: str) -> AsyncEngine:
    if database_url.startswith("sqlite+aiosqlite://"):
        return create_async_engine(
            url=database_url,
            echo=False,
        )
    return create_async_engine(
        url=database_url,
        echo=False,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=5,
    )


def create_session_factory(
    async_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=async_engine)


engine = create_database_engine(settings.database_url)
session_factory = create_session_factory(engine)
