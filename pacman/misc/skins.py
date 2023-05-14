from typing import Union

from pacman.data_core import Dirs
from pacman.misc.animator.animator import Animator
from pacman.misc.animator.sprite_animator import SpriteSheetAnimator
from pacman.misc.animator.sprite_sheet import sprite_slice, advanced_sprite_slice
from pacman.misc.serializers import SkinStorage
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
        walk = advanced_sprite_slice(f"{Dirs.IMAGE}/pacman/{self.name}/walk", (13, 13))
        return SpriteSheetAnimator(walk)

    @property
    def dead(self):
        dead = sprite_slice(f"pacman/{self.name}/dead", (15, 15))
        return Animator(dead, 100, False)

    @property
    def image(self):
        return self.__image

    def prerender_surface(self) -> ImageObject:
        img = sprite_slice(f"pacman/{self.name}/walk", (13, 13))[0]
        return ImageObject(img, (145, 125)).scale(70, 70)

    def __str__(self):
        return self.name


class Skins:
    def __init__(self):
        self.default = Skin("default", {})
        self.edge = Skin("edge", {0: 12, 1: 5})
        self.pokeball = Skin("pokeball", {2: 12, 3: 5})
        self.windows = Skin("windows", {3: 12, 4: 5})
        self.half_life = Skin("half_life", {4: 12, 5: 5})
        self.chrome = Skin("chrome", {5: 12, 6: 5})
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
