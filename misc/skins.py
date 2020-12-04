from typing import Union, Dict
import pygame as pg

from misc import Animator, get_list_path, get_path


class Skins:
    class __Skin:

        def __init__(self, skin_name):
            self.name = skin_name
            self.walk = Animator(get_list_path('png', 'images', 'pacman', self.name, 'walk'))
            self.dead = Animator(get_list_path('png', 'images', 'pacman', self.name, 'dead'), 100, False, True)
            self.__surface = self.prerender_surface()

        @property
        def surface(self):
            return self.__surface

        def prerender_surface(self) -> pg.Surface:
            return pg.image.load(get_path('1', 'png', 'images', 'pacman', self.name, 'walk'))

    def __init__(self):
        """
        param must be named like folder with skin
        """
        self.default = None
        self.chrome = None
        self.half_life = None
        self.load_skins()

        self.__current = self.default
        self.__prerenders = self.prerender_surfaces()

    def prerender_surfaces(self) -> Dict[str, pg.Surface]:
        return {key: self.__dict__[key].surface for key in self.all_skins}

    def load_skins(self) -> None:
        for key in self.__dict__.keys():
            if not key.startswith("_"):
                self.__dict__[key] = self.__Skin(key)

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
    def current(self, value: Union[str, __Skin]):
        if isinstance(value, str):
            self.__current = self.__dict__[value]
        elif isinstance(value, self.__Skin):
            self.__current = value
