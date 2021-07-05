from threading import Thread

import pygame as pg
from typing import NamedTuple, List
from misc.path import get_path, get_list_path
import time as tm


class Sounds:
    pg.mixer.init()
    __loading_text: str = ''
    __game = None
    __counter = 0
    __count = 32
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

    @staticmethod
    def load(key, attr):
        if hasattr(Sounds, key):
            setattr(Sounds, key, attr())
            Sounds.loading()

    @staticmethod
    def load_sounds(loading_text, game):
        func = {
            'CLICK': lambda: pg.mixer.Sound(get_path('navigation', 'ogg', 'sounds')),
            "SEED": lambda: pg.mixer.Sound(get_path('munch', 'ogg', 'sounds')),
            "SEED_FUN": lambda: pg.mixer.Sound(get_path('leader', 'ogg', 'sounds')),
            "FRUIT": lambda: pg.mixer.Sound(get_path('eat_fruit', 'ogg', 'sounds')),
            "GHOST": lambda: pg.mixer.Sound(get_path('eat_ghost', 'ogg', 'sounds')),
            "POC_INTRO": lambda: pg.mixer.Sound(get_path("pokemon_intro", 'ogg', 'sounds')),
            "INTERMISSION": lambda: pg.mixer.Sound(get_path('intermission', 'ogg', 'sounds')),
            "PELLET": lambda: pg.mixer.Sound(get_path('power_pellet', 'ogg', 'sounds')),
            "CHEAT": lambda: pg.mixer.Sound(get_path('cheat', 'ogg', 'sounds')),
            "DEAD": lambda: [pg.mixer.Sound(path) for path in get_list_path('ogg', 'sounds', 'death')],
            "GAMEOVER": lambda: [pg.mixer.Sound(path) for path in get_list_path('ogg', 'sounds', 'gameover')],
            "INTRO": lambda: [pg.mixer.Sound(path) for path in get_list_path('ogg', 'sounds', 'intro')],
            "SIREN": lambda: [pg.mixer.Sound(path) for path in get_list_path('ogg', 'sounds', 'siren')],
            "VALVE_SOUNDS": lambda: [pg.mixer.Sound(path) for path in get_list_path('ogg', 'sounds', 'valve_skin')],
            "WINDOWS_SOUNDS": lambda: [pg.mixer.Sound(path) for path in get_list_path('ogg', 'sounds', 'windows_skin')],
        }
        Sounds.__game = game
        Sounds.__loading_text = loading_text
        threads = [Thread(target=Sounds.load, args=(key, attr)) for key, attr in func.items()]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        for path in get_list_path('ogg', 'sounds', 'credits'):
            Sounds.loading()
            Sounds.CREDITS.append(pg.mixer.Sound(path))

        # Sounds.CLICK = pg.mixer.Sound(get_path('navigation', 'ogg', 'sounds'))
        #
        # Sounds.SEED = pg.mixer.Sound(get_path('munch', 'ogg', 'sounds'))
        # Sounds.loading()
        # Sounds.SEED_FUN = pg.mixer.Sound(get_path('leader', 'ogg', 'sounds'))
        # Sounds.loading()
        # Sounds.FRUIT = pg.mixer.Sound(get_path('eat_fruit', 'ogg', 'sounds'))
        # Sounds.loading()
        # Sounds.GHOST = pg.mixer.Sound(get_path('eat_ghost', 'ogg', 'sounds'))
        # Sounds.loading()
        # Sounds.POC_INTRO = pg.mixer.Sound(get_path("pokemon_intro", 'ogg', 'sounds'))
        # Sounds.loading()
        # Sounds.INTERMISSION = pg.mixer.Sound(get_path('intermission', 'ogg', 'sounds'))
        # Sounds.loading()
        # Sounds.PELLET = pg.mixer.Sound(get_path('power_pellet', 'ogg', 'sounds'))
        # Sounds.loading()
        # Sounds.CHEAT = pg.mixer.Sound(get_path('cheat', 'ogg', 'sounds'))
        # Sounds.loading()
        # Sounds.DEAD = [pg.mixer.Sound(path) for path in get_list_path('ogg', 'sounds', 'death')]
        # Sounds.loading()
        # Sounds.GAMEOVER = [pg.mixer.Sound(path) for path in get_list_path('ogg', 'sounds', 'gameover')]
        # Sounds.loading()
        # Sounds.INTRO = [pg.mixer.Sound(path) for path in get_list_path('ogg', 'sounds', 'intro')]
        # Sounds.loading()
        # Sounds.SIREN = [pg.mixer.Sound(path) for path in get_list_path('ogg', 'sounds', 'siren')]
        # Sounds.loading()

        # Sounds.loading()
        # # valve
        # Sounds.VALVE_SOUNDS = [pg.mixer.Sound(path) for path in get_list_path('ogg', 'sounds', 'valve_skin')]
        # Sounds.loading()
        # # windows
        # Sounds.WINDOWS_SOUNDS = [pg.mixer.Sound(path) for path in get_list_path('ogg', 'sounds', 'windows_skin')]

    @staticmethod
    def loading():
        pg.event.get()
        Sounds.__counter += 1
        Sounds.__loading_text = f"Loading {int((Sounds.__counter / Sounds.__count) * 100)}%"
        Sounds.__game.screen.fill(Color.BLACK)
        Sounds.__game.draw_load_img(Sounds.__loading_text)


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


def if_else(priority, secondary):
    return priority if priority else secondary
