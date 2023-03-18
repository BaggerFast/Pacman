from abc import ABC
from typing import Final

import pygame as pg

from pacman.data_core import PathManager, Dirs


class KbKeys(ABC):
    UP: Final = (pg.K_UP, pg.K_w)
    DOWN: Final = (pg.K_DOWN, pg.K_s)
    LEFT: Final = (pg.K_LEFT, pg.K_d)
    RIGHT: Final = (pg.K_RIGHT, pg.K_a)
    ENTER: Final = (pg.K_SPACE, pg.K_RETURN)


class Colors(ABC):
    RED: Final = pg.Color("red")
    BLUE: Final = pg.Color("blue")
    GREEN: Final = pg.Color("green")
    BLACK: Final = pg.Color("black")
    WHITE: Final = pg.Color("white")
    ORANGE: Final = pg.Color("orange")
    YELLOW: Final = pg.Color("yellow")
    GOLD: Final = pg.Color("gold")
    GRAY: Final = pg.Color("gray50")
    DARK_GRAY: Final = pg.Color("gray26")
    SILVER: Final = pg.Color(192, 192, 192)
    BRONZE: Final = pg.Color(205, 127, 50)
    WOODEN: Final = pg.Color(101, 67, 33)
    JET: Final = pg.Color(10, 10, 10, 120)
    MAIN_MAP: Final = pg.Color(33, 33, 255)
    DARK_RED: Final = pg.Color(125, 0, 0)
    DARK_GREEN: Final = pg.Color(0, 125, 0)
    HALF_TRANSPARENT: Final = pg.Color(0, 0, 0, 40)
    TRANSPARENT: Final = pg.Color(0, 0, 0, 0)


class Sounds(ABC):
    CLICK: Final[str] = "navigation"
    SEED: Final[str] = "munch"
    SEED_FUN: Final[str] = "leader"
    FRUIT: Final[str] = "eat_fruit"
    GHOST: Final[str] = "eat_ghost"
    POC_INTRO: Final[str] = "pokemon_intro"
    INTERMISSION: Final[str] = "intermission"
    PELLET: Final[str] = "power_pellet"

    DEAD = PathManager.get_list_path(f"{Dirs.SOUND}/death", ext="ogg")
    GAME_OVER = PathManager.get_list_path(f"{Dirs.SOUND}/gameover", ext="ogg")
    INTRO = PathManager.get_list_path(f"{Dirs.SOUND}/intro", ext="ogg")
    SIREN = PathManager.get_list_path(f"{Dirs.SOUND}/siren", ext="ogg")
