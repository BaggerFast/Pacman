import os
import sys
import pygame as pg
from typing import Final
from abc import ABC


VERSION: Final = '1.0.3'
DEBUG: Final = 'debug' in sys.argv

CELL_SIZE: Final = 8
FRUITS_COUNT: Final = 8
FPS: Final = 60


class Dir(ABC):
    BASE: Final = os.path.dirname(os.path.abspath(__file__))
    ASSET: Final = os.path.join(BASE, 'assets')
    IMAGE: Final = os.path.join(ASSET, 'images')
    SOUND: Final = os.path.join(ASSET, 'sounds')
    LOG: Final = os.path.join(BASE, 'logs')


class Keyboard(ABC):
    RIGHT: Final = (pg.K_d, pg.K_RIGHT)
    LEFT: Final = (pg.K_a, pg.K_LEFT)
    UP: Final = (pg.K_w, pg.K_UP)
    DOWN: Final = (pg.K_s, pg.K_DOWN)
    ENTER: Final = (pg.K_SPACE, pg.K_RETURN)
