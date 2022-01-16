import pygame as pg
from typing import NamedTuple, Callable
from misc.path import get_path, get_list_path


def load_sound(name: str):
    return pg.mixer.Sound(get_path(f'sounds/{name}'))


def load_list_sounds(name: str):
    return [pg.mixer.Sound(path) for path in get_list_path(f'sounds/{name}', ext='ogg')]


class Sounds:
    pg.mixer.init()

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

    class Ch:
        pacman: int = 0
        intro: int = 1
        game_over = menu = 2
        siren: int = 3
        seed = ghost = fruit = 4
        pellet: int = 5


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


class MenuPreset(NamedTuple):
    header: str
    function: Callable
