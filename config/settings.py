import os
import sys
import pygame as pg
from typing import NamedTuple

VERSION = '1.0.3'
DEBUG = 'debug' in sys.argv


class Dir(NamedTuple):
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ASSET = os.path.join(BASE, 'assets')
    IMAGE = os.path.join(ASSET, 'images')
    SOUND = os.path.join(ASSET, 'sounds')


class Keyboard(NamedTuple):
    RIGHT = (pg.K_d, pg.K_RIGHT)
    LEFT = (pg.K_a, pg.K_LEFT)
    UP = (pg.K_w, pg.K_UP)
    DOWN = (pg.K_s, pg.K_DOWN)
    ENTER = (pg.K_SPACE, pg.K_RETURN)
