from random import randint

from pygame import KEYDOWN, K_ESCAPE


def is_esc_pressed(event):
    return event.type == KEYDOWN and event.key == K_ESCAPE


def rand_color(brightness: int = 75) -> tuple[int, int, int]:
    while True:
        red = randint(0, 255)
        green = randint(0, 255)
        blue = randint(0, 255)
        bright = (red * 299 + green * 587 + blue * 114) / 1000
        if bright > brightness:
            return red, green, blue
