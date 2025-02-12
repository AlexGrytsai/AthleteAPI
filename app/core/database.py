import logging
import socket

from asyncpg.exceptions import (
    InvalidAuthorizationSpecificationError,
    InvalidCatalogNameError,
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from app.core.config import settings
from app.core.exceptions import (
    InvalidUsernameOrPasswordForDatabase,
    WrongDatabaseName,
    DatabaseConnectionErrorWrongHostOrPort,
    ProblemWithConnectionToDatabaseServer,
)

logger = logging.getLogger(__name__)


async def create_database_engine() -> AsyncEngine:
    try:
        engine = create_async_engine(
            url=settings.database_url,
            echo=False,
            pool_size=5,
            max_overflow=10,
        )
        async with engine.connect():
            return engine
    except socket.gaierror as exc:
        error_message = (
            f"Was provided invalid host or port "
            f"for connection to Database. Trigger exception: "
            f"{exc.__class__.__name__}.\n"
            f"Message: {exc}"
        )
        raise DatabaseConnectionErrorWrongHostOrPort(error_message)
    except InvalidAuthorizationSpecificationError as exc:
        error_message = (
            f"Was provided invalid username or password "
            f"for connection to Database. Trigger exception: "
            f"{exc.__class__.__name__}.\n"
            f"Message: {exc}"
        )
        logger.error(error_message)
        raise InvalidUsernameOrPasswordForDatabase(error_message)
    except InvalidCatalogNameError as exc:
        error_message = (
            f"Was provided wrong database name. Trigger exception: "
            f"{exc.__class__.__name__}.\n"
            f"Message: {exc}"
        )
        logger.error(error_message)
        raise WrongDatabaseName(error_message)
    except ConnectionRefusedError as exc:
        error_message = (
            f"Problem with connection to a remote computer. Trigger exception: "
            f"{exc.__class__.__name__}.\n"
            f"Message: {exc}"
        )
        logger.error(error_message)
        raise ProblemWithConnectionToDatabaseServer(error_message)
