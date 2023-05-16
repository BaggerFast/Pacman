from random import randint

from pygame import KEYDOWN, K_ESCAPE


def is_esc_pressed(event):
    return event.type == KEYDOWN and event.key == K_ESCAPE


def rand_color() -> tuple[int, int, int]:
    max_states = 7
    min_val = 200
    max_val = 230
    state = randint(0, max_states)
    if state == max_states:
        color = (255, 255, 255)
    elif state == max_states - 1:
        color = (randint(min_val, max_val), 0, 0)
    elif state == max_states - 2:
        color = (0, randint(min_val, max_val), 0)
    elif state == max_states - 3:
        color = (0, 0, randint(min_val, max_val))
    else:
        excluded_color = randint(0, 2)
        color = (
            randint(min_val, max_val) if excluded_color != 0 else 0,
            randint(min_val, max_val) if excluded_color != 1 else 0,
            randint(min_val, max_val) if excluded_color != 2 else 0,
        )
    return color
