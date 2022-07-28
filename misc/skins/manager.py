import pygame as pg

from misc.skins.skin import Skin


class Skins:

    def __init__(self, game):
        """
        param must be named like folder with skins
        """
        self.__skins_cost = {"default": {0: 0, 1: 0},
                             "half_life": {1: 14, 2: 10},
                             "windows": {2: 12, 3: 8},
                             "pokeball": {3: 10, 4: 7},
                             "edge": {4: 7, 5: 6},
                             "chrome": {6: 5, 7: 4}}
        self.__game = game
        self.default = Skin(self.__game)
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

    def prerender_surfaces(self) -> dict[str, pg.Surface]:
        return {key: self.__dict__[key].image for key in self.all_skins}

    def load_skins(self) -> None:
        for key in self.__dict__.keys():
            if not key.startswith("_"):
                self.__dict__[key] = Skin(self.__game, key)
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
    def current(self, value: str | Skin):
        if isinstance(value, str):
            self.__current = self.__dict__[value]
        elif isinstance(value, Skin):
            self.__current = value
