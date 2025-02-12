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
    critical_errors = {
        socket.gaierror: (
            DatabaseConnectionErrorWrongHostOrPort,
            "Was provided invalid host or port",
        ),
        InvalidAuthorizationSpecificationError: (
            InvalidUsernameOrPasswordForDatabase,
            "Was provided invalid username or password",
        ),
        InvalidCatalogNameError: (
            WrongDatabaseName,
            "Was provided wrong database name",
        ),
        ConnectionRefusedError: (
            ProblemWithConnectionToDatabaseServer,
            "Problem with connection to a remote computer",
        ),
    }

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            engine = await func(*args, **kwargs)
            await is_connected_to_database(engine)
            return engine
        except tuple(critical_errors.keys()) as exc:
            for base_exception in critical_errors:
                if isinstance(exc, base_exception):
                    error_class, message = critical_errors[base_exception]
                    break
            else:
                error_class, message = Exception, "Unknown database error"
            full_message = (
                f"{message}. Trigger exception: {exc.__class__}.\n"
                f"Message: {exc}"
            )

            logger.error(full_message)

            raise error_class(full_message)

    return wrapper
