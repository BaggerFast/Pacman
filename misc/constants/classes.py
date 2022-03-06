from typing import NamedTuple, Callable
import pygame as pg
from meta_classes import Singleton
from misc.path import get_path, get_list_path


def load_sound(name: str):
    return pg.mixer.Sound(get_path(f'assets/sounds/{name}'))


def load_list_sounds(name: str):
    return [pg.mixer.Sound(path) for path in get_list_path(f'assets/sounds/{name}', ext='ogg')]


class Sounds:
    pg.mixer.init()

    class Ch:
        # todo fix channels
        pacman = 1
        intro = 2
        game_over = menu = 3
        siren = 4
        eatable = 5
        pellet = 6

    CLICK = load_sound('navigation.ogg')
    SEED = load_sound('munch.ogg')
    SEED_FUN = load_sound('leader.ogg')
    FRUIT = load_sound('eat_fruit.ogg')
    GHOST = load_sound('eat_ghost.ogg')
    POC_INTRO = load_sound('pokemon_intro.ogg')
    INTERMISSION = load_sound('intermission.ogg')
    PELLET = load_sound('power_pellet.ogg')
    CHEAT = load_sound('cheat.ogg')
    DEAD = load_list_sounds('death')
    GAMEOVER = load_list_sounds('gameover')
    INTRO = load_list_sounds("intro")
    SIREN = load_list_sounds("siren")
    CREDITS = load_list_sounds('credits')
    VALVE_SOUNDS = load_list_sounds('valve_skin')
    WINDOWS_SOUNDS = load_list_sounds('windows_skin')


# class Sounds3(metaclass=SingletonMeta):
#     class Ch:
#         # todo fix channels
#         pacman = 1
#         intro = 2
#         game_over = menu = 3
#         siren = 4
#         eatable = 5
#         pellet = 6
#
#     def __init__(self):
#         self.CLICK = load_sound('navigation.ogg')
#         self.SEED = load_sound('munch.ogg')
#         self.SEED_FUN = load_sound('leader.ogg')
#         self.FRUIT = load_sound('eat_fruit.ogg')
#         self.GHOST = load_sound('eat_ghost.ogg')
#         self.POC_INTRO = load_sound('pokemon_intro.ogg')
#         self.INTERMISSION = load_sound('intermission.ogg')
#         self.PELLET = load_sound('power_pellet.ogg')
#         self.CHEAT = load_sound('cheat.ogg')
#         self.DEAD = load_list_sounds('death')
#         self.GAMEOVER = load_list_sounds('gameover')
#         self.INTRO = load_list_sounds("intro")
#         self.SIREN = load_list_sounds("siren")
#         self.CREDITS = load_list_sounds('credits')
#         self.VALVE_SOUNDS = load_list_sounds('valve_skin')
#         self.WINDOWS_SOUNDS = load_list_sounds('windows_skin')


class Color(NamedTuple):
    RED = pg.Color('red')
    BLUE = pg.Color('blue')
    GREEN = pg.Color('green')
    BLACK = pg.Color('black')
    WHITE = pg.Color('white')
    ORANGE = pg.Color('orange')
    YELLOW = pg.Color('yellow')
    GOLD = pg.Color('gold')
    GRAY = pg.Color('gray50')
    DARK_GRAY = pg.Color('gray26')
    SILVER = pg.Color(192, 192, 192)
    BRONZE = pg.Color(205, 127, 50)
    WOODEN = pg.Color(101, 67, 33)
    JET = pg.Color(10, 10, 10, 120)
    MAIN_MAP = pg.Color(33, 33, 255)
    DARK_RED = pg.Color(125, 0, 0)
    DARK_GREEN = pg.Color(0, 125, 0)
    HALF_TRANSPERENT = pg.Color(0, 0, 0, 40)
    TRANSPERENT = pg.Color(0, 0, 0, 0)


class Points:
    POINT_PER_SEED = 10
    POINT_PER_ENERGIZER = 50
    POINT_PER_FRUIT = 40


class Font:
    TITLE = get_path('assets/fonts/title.ttf')
    DEFAULT = get_path('assets/fonts/default.ttf')
    # todo refactor
    MAIN_SCENE_SIZE = 10
    BUTTON_TEXT_SIZE = 24
    BUTTON_FOR_SKINS_TEXT_SIZE = 16
    CREDITS_SCENE_SIZE = 14


class MenuPreset(NamedTuple):
    header: str
    function: Callable
