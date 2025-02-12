import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from app.utils.decorators import database_health_check

logger = logging.getLogger(__name__)


@database_health_check
async def create_database_engine(database_url: str) -> AsyncEngine:
    return create_async_engine(
        url=database_url,
        echo=False,
        pool_size=5,
        max_overflow=10,
    )
