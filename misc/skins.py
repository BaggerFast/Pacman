from copy import copy
from typing import Union, Dict
import pygame as pg

from data_core import PathManager, Dirs
from misc import Animator
from objects import ImageObject


class Skins:
    class Skin:
        def __init__(self, game, skin_name: str = "default"):
            self.name = skin_name
            self.skin_cost = {}
            self.__game = game
            self.__walk = Animator(
                PathManager.get_list_path(f"{Dirs.IMAGE}/pacman/{self.name}/walk", ext="png"),
            )
            self.__dead = Animator(
                PathManager.get_list_path(f"{Dirs.IMAGE}/pacman/{self.name}/dead", ext="png"),
                100, False, True)
            self.__image = self.prerender_surface()

        @property
        def is_unlocked(self):
            return self.name in self.__game.unlocked_skins

        @property
        def walk(self):
            return copy(self.__walk)

        @property
        def dead(self):
            return copy(self.__dead)

        @property
        def image(self):
            return self.__image

        def prerender_surface(self) -> pg.Surface:
            image = ImageObject(
                self.__game,
                pg.image.load(PathManager.get_image_path(f"pacman/{self.name}/walk/1")),
                (145, 125),
            )
            image.scale(70, 70)
            return image

    def __init__(self, game):
        self.__skins_cost = {
            "default": {0: 0, 1: 0},
            "half_life": {1: 14, 2: 10},
            "windows": {2: 12, 3: 8},
            "pokeball": {3: 10, 4: 7},
            "edge": {4: 7, 5: 6},
            "chrome": {6: 5, 7: 4},
        }
        self.__game = game
        self.default = self.Skin(self.__game)
        self.half_life = None
        self.pokeball = None
        self.edge = None
        self.chrome = None
        self.windows = None
        self.load_skins()

        self.__current = self.default
        self.__prerenders = self.prerender_surfaces()

    @property
    def skins_cost(self):
        return self.__skins_cost

    def prerender_surfaces(self) -> Dict[str, pg.Surface]:
        return {key: self.__dict__[key].image for key in self.all_skins}

    def load_skins(self) -> None:
        for key in self.__dict__.keys():
            if not key.startswith("_"):
                self.__dict__[key] = self.Skin(self.__game, key)
                self.__dict__[key].skin_cost = self.__skins_cost[key]

    @property
    def prerenders(self):
        return self.__prerenders

    @property
    def all_skins(self):
        return [key for key in self.__dict__.keys() if not key.startswith("_")]

    @property
    def names(self):
        return [key for key in self.__dict__.keys() if not key.startswith("_")]

    @property
    def current(self):
        return self.__current

    @current.setter
    def current(self, value: Union[str, Skin]):
        if isinstance(value, str):
            self.__current = self.__dict__[value]
        elif isinstance(value, self.Skin):
            self.__current = value
