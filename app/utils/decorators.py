import functools
import logging
import socket
import sys
import time
from collections import deque
from typing import Callable, Any

from asyncpg import (
    InvalidAuthorizationSpecificationError,
    InvalidCatalogNameError,
)
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncEngine

from app.core.exceptions import (
    DatabaseConnectionErrorWrongHostOrPort,
    InvalidUsernameOrPasswordForDatabase,
    WrongDatabaseName,
    ProblemWithConnectionToDatabaseServer,
)
from app.utils.memory_analysis import memory_report

logger = logging.getLogger(__name__)


def async_timer_of_execution(func: Callable) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()

        logger.info(
            f"Execution time for '{func.__name__}': "
            f"{end_time - start_time:.4f} seconds"
        )
        return result

    return wrapper


def sync_timer_of_execution(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        logger.info(
            f"Execution time for '{func.__name__}': "
            f"{end_time - start_time:.4f} seconds"
        )
        return result

    return wrapper


def memory_profiler_class(cls: Any) -> None:
    orig_init = cls.__init__

    @functools.wraps(orig_init)
    def new_init(self, *args, **kwargs) -> None:
        orig_init(self, *args, **kwargs)
        memory_report(self)

    cls.__init__ = new_init
    return cls


def memory_profiler_func(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"\n🔍 Analyzing memory for function: {func.__name__}")
        memory_report(result)
        return result

    return wrapper


async def is_connected_to_database(engine_instate: AsyncEngine) -> bool:
    try:
        async with engine_instate.connect():
            return True
    except DatabaseError:
        return False


def database_health_check(func: Callable) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            engine = await func(*args, **kwargs)
            await is_connected_to_database(engine)
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

    return wrapper
