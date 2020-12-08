import pygame as pg
from typing import NamedTuple, Union, List

from misc.path import get_path, get_list_path


class Sounds:
    class Tuple(NamedTuple):
        mixer: pg.mixer.Sound

    class TupleList(NamedTuple):
        list: list

    pg.mixer.init()
    CLICK = Tuple(pg.mixer.Sound(get_path('navigation', 'mp3', 'sounds'))).mixer
    SEED = Tuple(pg.mixer.Sound(get_path('munch', 'mp3', 'sounds'))).mixer
    SEED_FUN = Tuple(pg.mixer.Sound(get_path('leader', 'mp3', 'sounds'))).mixer
    FRUIT = Tuple(pg.mixer.Sound(get_path('eat_fruit', 'mp3', 'sounds'))).mixer
    GHOST = Tuple(pg.mixer.Sound(get_path('eat_ghost', 'mp3', 'sounds'))).mixer
    POC_INTRO = Tuple(pg.mixer.Sound(get_path("pocemon_intro", 'mp3', 'sounds'))).mixer
    INTERMISSION = Tuple(pg.mixer.Sound(get_path('intermission', 'mp3', 'sounds'))).mixer
    PELLET = Tuple(pg.mixer.Sound(get_path('power_pellet', 'mp3', 'sounds'))).mixer
    DEAD = TupleList(get_list_path('mp3', 'sounds', 'death')).list
    GAMEOVER = TupleList(get_list_path('mp3', 'sounds', 'gameover')).list
    INTRO = TupleList(get_list_path('mp3', 'Sounds', 'intro')).list
    SIREN = TupleList(get_list_path('mp3', 'sounds', 'siren')).list
    CREDITS = TupleList(get_list_path('mp3', 'sounds', 'credits')).list



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
    JET = Tuple(pg.Color(10, 10, 10, 120)).color
    MAIN_MAP = Tuple(pg.Color(33, 33, 255)).color
    DARK_RED = Tuple(pg.Color(125, 0, 0)).color
    DARK_GREEN = Tuple(pg.Color(0, 125, 0)).color
    HALF_TRANSPERENT = Tuple(pg.Color(0, 0, 0, 40)).color
    TRANSPERENT = Tuple(pg.Color(0, 0, 0, 0)).color


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
    BUTTON_FOR_SKINS_TEXT_SIZE = Tuple(size=16).size
    CREDITS_SCENE_SIZE = Tuple(size=14).size
