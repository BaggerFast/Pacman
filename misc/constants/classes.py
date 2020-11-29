import pygame as pg
from typing import NamedTuple

from misc.path import get_path


class Sounds:
    class Tuple(NamedTuple):
        mixer: pg.mixer.Sound
    pg.mixer.init()
    CLICK = Tuple(pg.mixer.Sound(get_path('sounds', 'NAV', 'wav'))).mixer
    DEAD = Tuple(pg.mixer.Sound(get_path('sounds', 'pacman_death', 'wav'))).mixer
    GAMEOVER = Tuple(pg.mixer.Sound(get_path('sounds', 'GameOver', 'wav'))).mixer
    BOOST = Tuple(pg.mixer.Sound(get_path('sounds', 'pacman_intermission', 'wav'))).mixer
    SEED = Tuple(pg.mixer.Sound(get_path('sounds', 'leader2', 'wav'))).mixer
    INTRO = Tuple(pg.mixer.Sound(get_path('sounds', 'pacman_beginning', 'wav'))).mixer
    MOVE = Tuple(pg.mixer.Sound(get_path('sounds', 'pacman_chomp', 'wav'))).mixer


class Color(NamedTuple):
    class Tuple(NamedTuple):
        color: pg.Color
    RED = Tuple(pg.Color('red')).color
    BLUE = Tuple(pg.Color('blue')).color
    GREEN = Tuple(pg.Color('green')).color
    BLACK = Tuple(pg.Color('black')).color
    WHITE = Tuple(pg.Color('white')).color
    ORANGE = Tuple(pg.Color('orange')).color
    YELLOW = Tuple(pg.Color('yellow')).color
    GOLD = Tuple(pg.Color('gold')).color
    GRAY = Tuple(pg.Color('gray50')).color
    DARK_GRAY = Tuple(pg.Color('gray26')).color
    SILVER = Tuple(pg.Color(192, 192, 192)).color
    BRONZE = Tuple(pg.Color(205, 127, 50)).color
    WOODEN = Tuple(pg.Color(101, 67, 33)).color
    JET = Tuple(pg.Color(10, 10, 10)).color


class Points:
    class Tuple(NamedTuple):
        value: int
    POINT_PER_SEED = Tuple(10).value
    POINT_PER_ENERGIZER = Tuple(50).value
    POINT_PER_FRUIT = Tuple(40).value


class Font:
    class Tuple(NamedTuple):
        size: int = 0
        font: str = ''
    TITLE = Tuple(font=get_path('fonts', 'font0', 'ttf')).font
    DEFAULT = Tuple(font=get_path('fonts', 'font1', 'ttf')).font
    MAIN_SCENE_SIZE = Tuple(size=10).size
    BUTTON_TEXT_SIZE = Tuple(size=24).size
    CREDITS_SCENE_SIZE = Tuple(size=14).size


class Maps(NamedTuple):
    class Tuple(NamedTuple):
        value: str
    level_1 = Tuple("original.json").value
    level_2 = Tuple("new_map.json").value
    level_3 = Tuple("new_new_map.json").value

    @staticmethod
    def get(attr: str) -> str:
        return getattr(Maps, attr)
