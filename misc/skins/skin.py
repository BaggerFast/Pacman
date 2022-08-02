from copy import copy

from misc import PathManager
from misc.animator import Animator
from misc.skins import SkinNames
from misc.storage import SkinStorage
from pacman.objects import ImageObject


class Skin:

    def __init__(self, skin_name: SkinNames, cost):
        self.name = skin_name
        self.skin_cost = cost,
        self.__walk = Animator(PathManager.get_list(f'{PathManager.IMAGE}/pacman/{self.name.name}/walk', ext='png'))
        self.__dead = Animator(PathManager.get_list(f'{PathManager.IMAGE}/pacman/{self.name.name}/dead', ext='png'),
                               100, False, True)
        self.__image = self.prerender_surface()

    @property
    def is_unlocked(self):
        return SkinStorage().is_unlock(self.name)

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
        image = ImageObject(f'pacman/{self.name.name}/walk/1.png', (145, 125))
        image.scale(70, 70)
        return image
