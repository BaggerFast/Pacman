from abc import ABC
from typing import Final

import pygame.locals as keys
from pygame import Color

from .data_classes import ResolutionSize
from .path_utl import PathUtl


class Cfg(ABC):
    FPS: Final[int] = 60
    RESOLUTION: Final = ResolutionSize(224, 285)
    TILE_SIZE: Final[int] = 8


class FontCfg(ABC):
    TITLE = PathUtl.get_asset("fonts/title.ttf")
    DEFAULT = PathUtl.get_asset("fonts/default.ttf")
    MAIN_SCENE_SIZE = 10
    BUTTON_TEXT_SIZE = 24
    BUTTON_FOR_SKINS_TEXT_SIZE = 16
    CREDITS_SCENE_SIZE = 14


class KbKeys(ABC):
    UP: Final = (keys.K_UP, keys.K_w)
    DOWN: Final = (keys.K_DOWN, keys.K_s)
    LEFT: Final = (keys.K_LEFT, keys.K_a)
    RIGHT: Final = (keys.K_RIGHT, keys.K_d)
    ENTER: Final = (keys.K_SPACE, keys.K_RETURN)


class Colors(ABC):
    RED: Final = Color("red")
    BLUE: Final = Color("blue")
    GREEN: Final = Color("green")
    BLACK: Final = Color("black")
    WHITE: Final = Color("white")
    ORANGE: Final = Color("orange")
    YELLOW: Final = Color("yellow")
    GOLD: Final = Color("gold")
    GRAY: Final = Color("gray50")
    DARK_GRAY: Final = Color("gray26")
    SILVER: Final = Color(192, 192, 192)
    BRONZE: Final = Color(205, 127, 50)
    WOODEN: Final = Color(101, 67, 33)
    JET: Final = Color(10, 10, 10, 120)
    MAIN_MAP: Final = Color(33, 33, 255)
    DARK_RED: Final = Color(125, 0, 0)
    DARK_GREEN: Final = Color(0, 125, 0)
    HALF_TRANSPARENT: Final = Color(0, 0, 0, 40)
    TRANSPARENT: Final = Color(0, 0, 0, 0)
