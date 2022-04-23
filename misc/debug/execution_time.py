import time
from config.settings import DEBUG


def check_execution_time(func):
    """decorator for recognize the speed of function execution in console (WORK ONLY IN DEBUG MODE)"""

    def wrapped(*args, **kwargs):
        if not DEBUG:
            return func(*args, **kwargs)
        start_time = time.monotonic()
        data = func(*args, **kwargs)
        print(f'{func.__qualname__}:{round(time.monotonic() - start_time, 3)}')
        return data
    return wrapped
