from random import randint

from pygame import K_ESCAPE, KEYDOWN, Surface, image
from pygame.mixer import Sound

from pacman.data_core import PathUtl


def is_esc_pressed(event) -> bool:
    return event.type == KEYDOWN and event.key == K_ESCAPE


def rand_color(brightness: int = 75) -> tuple[int, int, int]:
    while True:
        red = randint(0, 255)
        green = randint(0, 255)
        blue = randint(0, 255)
        bright = (red * 299 + green * 587 + blue * 114) / 1000
        if bright > brightness:
            return red, green, blue


def load_image(image_path: str, extension: str = "png") -> Surface:
    return image.load(PathUtl.get_img(image_path, extension))


def load_sound(sound_path: str, extension: str = "ogg") -> Sound:
    return Sound(PathUtl.get_sound(sound_path, extension))
