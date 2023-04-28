from copy import copy
from typing import Union
import pygame as pg
from pacman.data_core import PathManager, Dirs
from pacman.misc import Animator
from pacman.misc.serializers import SkinStorage
from pacman.misc.sprite_sheet import sprite_slice
from pacman.objects import ImageObject


class Skin:
    def __init__(self, skin_name: str, skin_cost):
        self.name = skin_name
        self.skin_cost = skin_cost
        self.__image = self.prerender_surface()

    @property
    def is_unlocked(self):
        return self.name in SkinStorage().unlocked

    @property
    def walk(self):
        return Animator(PathManager.get_list_path(f"{Dirs.IMAGE}/pacman/{self.name}/walk", ext="png"))

    @property
    def dead(self):
        dead = sprite_slice(pg.image.load(PathManager.get_image_path(f"pacman/{self.name}/dead")), (15, 15))
        return Animator(dead, 100, False, True)

    @property
    def image(self):
        return self.__image

    def prerender_surface(self) -> ImageObject:
        return ImageObject(
            pg.image.load(PathManager.get_image_path(f"pacman/{self.name}/walk/1")),
            (145, 125),
        ).scale(70, 70)

    def __str__(self):
        return self.name


class Skins:
    def __init__(self):
        self.default = Skin("default", {0: 0, 1: 0})
        self.edge = Skin("edge", {4: 7, 5: 6})
        self.pokeball = Skin("pokeball", {3: 10, 4: 7})
        self.windows = Skin("windows", {2: 12, 3: 8})
        self.half_life = Skin("half_life", {1: 14, 2: 10})
        self.chrome = Skin("chrome", {6: 5, 7: 4})
        self.__current = self.default

    @property
    def current(self):
        return self.__current

    @current.setter
    def current(self, value: Union[str, Skin]):
        if isinstance(value, str):
            self.__current = self.__dict__[value]
        if isinstance(value, Skin):
            self.__current = value
