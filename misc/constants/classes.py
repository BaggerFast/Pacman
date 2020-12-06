import pygame as pg
from typing import NamedTuple, Union, List

from misc.path import get_path, get_list_path


class Sounds:
    class Tuple(NamedTuple):
        mixer: pg.mixer.Sound

    class TupleList(NamedTuple):
        list: list

    pg.mixer.init()
    CLICK = Tuple(pg.mixer.Sound(get_path('navigation', 'wav', 'sounds'))).mixer
    DEAD = Tuple(pg.mixer.Sound(get_path('death', 'wav', 'sounds'))).mixer
    GAMEOVER = TupleList(get_list_path('wav', 'Sounds', 'gameover')).list
    SEED = Tuple(pg.mixer.Sound(get_path('munch', 'wav', 'sounds'))).mixer
    INTRO = TupleList(get_list_path('wav', 'Sounds', 'intro')).list
    MOVE = Tuple(pg.mixer.Sound(get_path('munch', 'wav', 'sounds'))).mixer
    SIREN = Tuple(pg.mixer.Sound(get_path('siren', 'wav', 'sounds'))).mixer
    FRUIT = Tuple(pg.mixer.Sound(get_path('eat_fruit', 'wav', 'sounds'))).mixer
    CREDITS = TupleList(get_list_path('wav', 'Sounds', 'credits')).list


class Color(NamedTuple):
    class Tuple(NamedTuple):
        color: pg.Color
        alpha: int = 0

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
    MAIN_MAP = Tuple(pg.Color(33, 33, 255)).color
    TRANSPERENT = Tuple(pg.Color(0, 0, 0, 50)).color


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

    TITLE = Tuple(font=get_path('title', 'ttf', 'fonts')).font
    DEFAULT = Tuple(font=get_path('default', 'ttf', 'fonts')).font
    MAIN_SCENE_SIZE = Tuple(size=10).size
    BUTTON_TEXT_SIZE = Tuple(size=24).size
    CREDITS_SCENE_SIZE = Tuple(size=14).size
