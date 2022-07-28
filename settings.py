from abc import ABC
from typing import Final

import pygame as pg

FPS: Final = 60
CELL_SIZE: Final = 8


class Keyboard(ABC):
    RIGHT: Final = (pg.K_d, pg.K_RIGHT)
    LEFT: Final = (pg.K_a, pg.K_LEFT)
    UP: Final = (pg.K_w, pg.K_UP)
    DOWN: Final = (pg.K_s, pg.K_DOWN)
    ENTER: Final = (pg.K_SPACE, pg.K_RETURN)
