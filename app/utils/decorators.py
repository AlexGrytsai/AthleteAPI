import logging
import time
from typing import Callable

logger = logging.getLogger(__name__)


def async_timer_of_execution(func: Callable) -> Callable:
    async def wrapper(*args, **kwargs):
        start_time = time.process_time()
        result = await func(*args, **kwargs)
        end_time = time.process_time()

        logger.info(
            f"Execution time for {func.__name__}: {end_time - start_time}"
        )
        return result

    return wrapper
