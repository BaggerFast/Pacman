from copy import copy
from typing import Union, Dict
import pygame as pg

from misc import Animator, get_path
from misc.animator import SpriteSheetAnimator
from misc.constants.skin_names import SkinsNames
from misc.sprite_sheet import SpriteSheet
from objects import ImageObject


class Skin:
    def __init__(self, game, path: str, cost: dict, skin_name: str = SkinsNames.default):
        self.name: str = skin_name
        self.skin_cost: dict = cost
        self.__game = game
        self.__walk = SpriteSheetAnimator(SpriteSheet(get_path(f'{path}/walk.png'), (13, 13)))
        self.__dead = Animator(SpriteSheet(get_path(f'{path}/dead.png'), (15, 15))[0],
                               time_out=125, repeat=True)
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

    def prerender_surface(self) -> ImageObject:
        image = ImageObject(self.__game, pg.image.load(get_path(f'images/pacman/{self.name}/1.png')),
                            (145, 125))
        image.scale(70, 70)
        return image


class Skins:
    def __init__(self, game):
        """
        param must be named like folder with skin
        """
        self.__game = game

        self.default = Skin(self.__game, f'images/pacman/default', {0: 0, 1: 0}, SkinsNames.default)
        self.half_life = Skin(self.__game, f'images/pacman/half_life', {1: 14, 2: 10}, SkinsNames.half_life)
        self.pokeball = Skin(self.__game, f'images/pacman/pokeball', {2: 12, 3: 8}, SkinsNames.pokeball)
        self.edge = Skin(self.__game, f'images/pacman/edge', {3: 10, 4: 7}, SkinsNames.edge)
        self.chrome = Skin(self.__game, f'images/pacman/chrome', {4: 7, 5: 6}, SkinsNames.chrome)
        self.windows = Skin(self.__game, f'images/pacman/windows', {6: 5, 5: 4}, SkinsNames.windows)

        self.__current = self.default
        self.__prerenders = self.prerender_surfaces()

    def prerender_surfaces(self) -> Dict[str, pg.Surface]:
        return {key: self.__dict__[key].image for key in self.all_skins}

    @property
    def all_skins(self):
        return [key for key in self.__dict__.keys() if not key.startswith("_")]

    @property
    def current(self):
        return self.__current

    @current.setter
    def current(self, value: Union[str, Skin]):
        if isinstance(value, str):
            self.__current = self.__dict__[value]
        elif isinstance(value, Skin):
            self.__current = value
