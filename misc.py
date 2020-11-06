from random import randint


def get_nonzero_random_value(max_abs_value: int) -> int:
    return randint(1, max_abs_value) if randint(0, 1) else randint(-max_abs_value, -1)