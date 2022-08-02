import pygame as pg

from misc.skins import SkinNames
from misc.skins.skin import Skin
from pacman.scenes.manager import SceneManager


class Skins:

    def __init__(self, game):
        """
        param must be named like folder with skins
        """
        self.__game = game
        self.default = Skin(SkinNames.DEFAULT, {0: 0, 1: 0})
        self.half_life = Skin(SkinNames.HALF_LIFE, {1: 14, 2: 10})
        self.pokeball = Skin(SkinNames.POKEBALL, {2: 12, 3: 8})
        self.edge = Skin(SkinNames.EDGE, {4: 7, 5: 6})
        self.chrome = Skin(SkinNames.CHROME, {6: 5, 7: 4})
        self.windows = Skin(SkinNames.WINDOWS, {3: 10, 4: 7})

        self.__current = self.default
        self.__prerenders = self.prerender_surfaces()

    def prerender_surfaces(self) -> dict[str, pg.Surface]:
        return {key: self.__dict__[key].image for key in self.all_skins}

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
    def current(self, value: str | Skin):
        if isinstance(value, str):
            self.__current = self.__dict__[value]
        elif isinstance(value, Skin):
            self.__current = value
