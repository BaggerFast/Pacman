import time


def time_of_func(func):
    def wrapped(*args, **kwargs):
        start_time = time.monotonic()
        func(*args, **kwargs)
        print(f'{func.__qualname__}:{round(time.monotonic() - start_time, 3)}')
    return wrapped
