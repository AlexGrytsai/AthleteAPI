import logging

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)

from app.core.config import settings
from app.utils.decorators import database_health_check

logger = logging.getLogger(__name__)


@database_health_check
def create_database_engine(database_url: str) -> AsyncEngine:
    return create_async_engine(
        url=database_url,
        echo=False,
        pool_size=5,
        max_overflow=10,
    )


def create_session_factory(
    async_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=async_engine)


engine = create_database_engine(settings.database_url)
session_factory = create_session_factory(engine)
