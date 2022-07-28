import pygame as pg

from misc.path_manager import PathManager


def load_image(path: str):
    return pg.image.load(PathManager.get_image(path))


def load_sound(path: str):
    return pg.mixer.Sound(PathManager.get_sound(path))
