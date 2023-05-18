from pygame import image, Surface

from pacman.data_core import PathUtil


def load_image(image_path: str, extension: str = "png") -> Surface:
    return image.load(PathUtil.get_img(image_path, extension))
