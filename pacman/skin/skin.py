from copy import copy

from pacman.animator import Animator, SpriteSheetAnimator, advanced_sprite_slice, sprite_slice
from pacman.misc import ImgObj


class Skin:
    def __init__(self, skin_name: str, skin_cost):
        dead_sprite = sprite_slice(f"pacman/{skin_name}/dead", (15, 15))
        walk_sprite = advanced_sprite_slice(f"pacman/{skin_name}/walk", (13, 13))

        self.name = skin_name
        self.skin_cost = skin_cost
        self.__dead_anim = Animator(dead_sprite, endless=False)
        self.__walk_anim = SpriteSheetAnimator(walk_sprite)

    @property
    def walk(self) -> SpriteSheetAnimator:
        return copy(self.__walk_anim)

    @property
    def dead(self) -> Animator:
        return copy(self.__dead_anim)

    def preview(self) -> ImgObj:
        return ImgObj(self.__walk_anim.current_image)
