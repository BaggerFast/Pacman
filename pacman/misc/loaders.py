from pygame import Surface, image
from pygame.mixer import Sound

from pacman.data_core import PathUtil


def load_image(image_path: str, extension: str = "png") -> Surface:
    return image.load(PathUtil.get_img(image_path, extension))


def load_sound(sound_path: str, extension: str = "ogg") -> Sound:
    return Sound(PathUtil.get_sound(sound_path, extension))
