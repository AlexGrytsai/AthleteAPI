import functools
import logging
import time
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
    from app.core.config import DEVELOP_MODE

    orig_init = cls.__init__

    @functools.wraps(orig_init)
    def new_init(self, *args, **kwargs) -> None:
        orig_init(self, *args, **kwargs)
        if DEVELOP_MODE:
            memory_report(self)

    cls.__init__ = new_init
    return cls


def memory_profiler_func(func: Callable) -> Callable:
    from app.core.config import DEVELOP_MODE

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if DEVELOP_MODE:
            print(f"\n🔍 Analyzing memory for function: {func.__name__}")
            memory_report(result)
        return result

    return wrapper
