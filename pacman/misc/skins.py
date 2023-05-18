from pacman.data_core import Dirs
from pacman.misc.animator.animator import Animator
from pacman.misc.animator.sprite_animator import SpriteSheetAnimator
from pacman.misc.animator.sprite_sheet import advanced_sprite_slice, sprite_slice
from pacman.objects import ImageObject


class Skin:
    def __init__(self, skin_name: str, skin_cost):
        self.name = skin_name
        self.skin_cost = skin_cost
        self.__image = self.prerender_surface()

    @property
    def walk(self):
        walk = advanced_sprite_slice(f"{Dirs.IMAGE}/pacman/{self.name}/walk", (13, 13))
        return SpriteSheetAnimator(walk)

    @property
    def dead(self):
        dead = sprite_slice(f"pacman/{self.name}/dead", (15, 15))
        return Animator(dead, repeat=False)

    @property
    def image(self):
        return self.__image

    def prerender_surface(self) -> ImageObject:
        img = sprite_slice(f"pacman/{self.name}/walk", (13, 13))[0]
        return ImageObject(img, (145, 125)).scale(70, 70)

    def __str__(self):
        return self.name
