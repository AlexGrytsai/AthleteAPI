import functools
import logging
import sys
import time
from collections import deque
from typing import Callable, Any

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
