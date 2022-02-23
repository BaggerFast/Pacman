import time


def check_execution_time(func):
    def wrapped(*args, **kwargs):
        start_time = time.monotonic()
        data = func(*args, **kwargs)
        print(f'{func.__qualname__}:{round(time.monotonic() - start_time, 3)}')
        return data
    return wrapped
