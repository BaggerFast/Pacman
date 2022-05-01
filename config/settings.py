import os
import sys
import pygame as pg

from typing import Final
from abc import ABC

VERSION = '1.0.3'
DEBUG = 'debug' in sys.argv


class Dir(ABC):
    BASE: Final = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ASSET: Final = os.path.join(BASE, 'assets')
    IMAGE: Final = os.path.join(ASSET, 'images')
    SOUND: Final = os.path.join(ASSET, 'sounds')


class Keyboard(ABC):
    RIGHT: Final = (pg.K_d, pg.K_RIGHT)
    LEFT: Final = (pg.K_a, pg.K_LEFT)
    UP: Final = (pg.K_w, pg.K_UP)
    DOWN: Final = (pg.K_s, pg.K_DOWN)
    ENTER: Final = (pg.K_SPACE, pg.K_RETURN)
