import pygame as pg
from typing import NamedTuple, List
from misc.path import get_path, get_list_path


class Sounds:
    __loading_text: str = ''
    __game = None
    __counter = 0
    __count = 100
    CLICK: pg.mixer.Sound = None
    SEED: pg.mixer.Sound = None
    SEED_FUN: pg.mixer.Sound = None
    FRUIT: pg.mixer.Sound = None
    GHOST: pg.mixer.Sound = None
    POC_INTRO: pg.mixer.Sound = None
    INTERMISSION: pg.mixer.Sound = None
    PELLET: pg.mixer.Sound = None
    CHEAT: pg.mixer.Sound = None
    DEAD: List[pg.mixer.Sound] = []
    GAMEOVER: List[pg.mixer.Sound] = []
    INTRO: List[pg.mixer.Sound] = []
    SIREN: List[pg.mixer.Sound] = []
    CREDITS: List[pg.mixer.Sound] = []
    # valve
    VALVE_SOUNDS: List[pg.mixer.Sound] = []
    # windows
    WINDOWS_SOUNDS: List[pg.mixer.Sound] = []

    class Ch:
        pacman: int = 0
        intro: int = 1
        game_over = menu = 2
        siren: int = 3
        seed = ghost = fruit = 4
        pellet: int = 5

    @staticmethod
    def load(key, attr):
        if hasattr(Sounds, key):
            attrs = attr()
            setattr(Sounds, key, attrs)

    @staticmethod
    def load_sounds():
        list_path = lambda path: [pg.mixer.Sound(path) for path in get_list_path(f'sounds/{path}', ext='ogg')]
        path = lambda path: pg.mixer.Sound(get_path(f'sounds/{path}'))
        func = {
            'CLICK': lambda: path('navigation.ogg'),
            "SEED": lambda: path('munch.ogg'),
            "SEED_FUN": lambda: path('leader.ogg'),
            "FRUIT": lambda: path('eat_fruit.ogg'),
            "GHOST": lambda: path('eat_ghost.ogg'),
            "POC_INTRO": lambda: path("pokemon_intro.ogg"),
            "INTERMISSION": lambda: path('intermission.ogg'),
            "PELLET": lambda:  path('power_pellet.ogg'),
            "CHEAT": lambda:  path('cheat.ogg'),
            "DEAD": lambda: list_path('death'),
            "GAMEOVER": lambda: list_path('gameover'),
            "INTRO": lambda: list_path("intro"),
            "SIREN": lambda: list_path("siren"),
            "VALVE_SOUNDS": lambda:  list_path('valve_skin'),
            "WINDOWS_SOUNDS": lambda: list_path('windows_skin'),
            "CREDITS": lambda: list_path('credits'),
        }
        [Sounds.load(key, attr) for key, attr in func.items()]


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

    TITLE = Tuple(font=get_path('fonts/title.ttf')).font
    DEFAULT = Tuple(font=get_path('fonts/default.ttf')).font
    MAIN_SCENE_SIZE = Tuple(size=10).size
    BUTTON_TEXT_SIZE = Tuple(size=24).size
    BUTTON_FOR_SKINS_TEXT_SIZE = Tuple(size=16).size
    CREDITS_SCENE_SIZE = Tuple(size=14).size
