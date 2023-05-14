from pygame import image

from pacman.data_core import PathManager


def load_image(image_path: str, extension: str = "png"):
    return image.load(PathManager.get_image_path(image_path, extension))
