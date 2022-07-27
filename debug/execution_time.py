import time
from loguru import logger


def check_execution_time(func):
    """decorator for recognize the speed of function execution in a console (WORK ONLY IN DEBUG MODE)"""

    def wrapped(*args, **kwargs):
        start_time = time.monotonic()
        data = func(*args, **kwargs)
        logger.debug(f'{func.__qualname__}:{round(time.monotonic() - start_time, 3)}')
        return data

    return wrapped
