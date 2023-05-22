from copy import copy

from pygame import Surface

from pacman.animator import Animator, SpriteSheetAnimator, advanced_sprite_slice, sprite_slice
from pacman.misc import ImgObj, load_image


class Skin:
    def __init__(self, skin_path_name: str, skin_cost, name: str = ""):
        if not name:
            self.__name = skin_path_name
        dead_sprite = sprite_slice(f"pacman/{skin_path_name}/dead", (15, 15))
        walk_sprite = advanced_sprite_slice(f"pacman/{skin_path_name}/walk", (13, 13))
        self.__aura = load_image(f"pacman/{skin_path_name}/aura")
        self.__cost = skin_cost
        self.__dead_anim = Animator(dead_sprite, endless=False)
        self.__walk_anim = SpriteSheetAnimator(walk_sprite)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def walk(self) -> SpriteSheetAnimator:
        return copy(self.__walk_anim)

    @property
    def dead(self) -> Animator:
        return copy(self.__dead_anim)

    @property
    def aura(self) -> Surface:
        return copy(self.__aura)

    @property
    def cost(self) -> dict:
        return self.__cost

    @property
    def preview(self) -> ImgObj:
        return ImgObj(self.__walk_anim.current_image)
