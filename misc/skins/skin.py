from copy import copy

from misc import PathManager
from misc.animator import Animator
from pacman.objects import ImageObject


class Skin:

    def __init__(self, game, skin_name: str = "default"):
        self.name = skin_name
        self.skin_cost = {}
        self.__game = game,
        self.__walk = Animator(PathManager.get_list(f'{PathManager.IMAGE}/pacman/{self.name}/walk', ext='png'))
        self.__dead = Animator(PathManager.get_list(f'{PathManager.IMAGE}/pacman/{self.name}/dead', ext='png'),
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

    def prerender_surface(self) -> ImageObject:
        image = ImageObject(self.__game, f'pacman/{self.name}/walk/1.png', (145, 125))
        image.scale(70, 70)
        return image
