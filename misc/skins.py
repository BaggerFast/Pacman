from copy import copy
from typing import Union, Dict
import pygame as pg

from misc import Animator, get_list_path, get_path
from objects import ImageObject


class Skins:
    class Skin:
        def __init__(self, game, skin_name: str = "default"):
            self.name = skin_name
            self.__game = game
            self.__walk = Animator(get_list_path('png', 'images', 'pacman', self.name, 'walk'))
            self.__dead = Animator(get_list_path('png', 'images', 'pacman', self.name, 'dead'), 100, False, True)
            self.__image = self.prerender_surface()

        @property
        def walk(self):
            return self.__walk

        @property
        def dead(self):
            return self.__dead

        @property
        def image(self):
            return self.__image

        def prerender_surface(self) -> pg.Surface:
            image = ImageObject(self.__game, pg.image.load(get_path('1', 'png', 'images', 'pacman', self.name, 'walk')), (130, 110))
            image.scale(75, 75)
            return image

    def __init__(self, game):
        """
        param must be named like folder with skin
        """
        self.__game = game
        self.default = self.Skin(self.__game)
        self.chrome = None
        self.half_life = None
        self.load_skins()

        self.__current = self.default
        self.__prerenders = self.prerender_surfaces()

    def prerender_surfaces(self) -> Dict[str, pg.Surface]:
        return {key: self.__dict__[key].image for key in self.all_skins}

    def load_skins(self) -> None:
        for key in self.__dict__.keys():
            if not key.startswith("_"):
                self.__dict__[key] = self.Skin(self.__game, key)

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
