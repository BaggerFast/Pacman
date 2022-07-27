import os
import pygame as pg

from typing import NamedTuple, Callable
from settings import Dir
from pacman.misc.path import PathManager


def load_sound(name: str):
    return pg.mixer.Sound(os.path.join(Dir.SOUND, name))


def load_list_sounds(name: str):
    return [pg.mixer.Sound(path) for path in PathManager.get_list_path(f'assets/sounds/{name}', ext='ogg')]


# todo Sounds remake
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

    CLICK = load_sound('ui/navigation.ogg')
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

    VALVE_SOUNDS = load_list_sounds('valve_skin')
    WINDOWS_SOUNDS = load_list_sounds('windows_skin')


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
    HALF_TRANSPERENT = pg.Color(0, 0, 0, 0)
    TRANSPERENT = pg.Color(0, 0, 0, 0)


class Font(NamedTuple):
    TITLE = PathManager.get_asset_path('fonts/title.ttf')
    DEFAULT = PathManager.get_asset_path('fonts/default.ttf')
    MAIN_SCENE_SIZE = 10
    CREDITS_SCENE_SIZE = 14
    BUTTON_TEXT_SIZE = 24
    BUTTON_FOR_SKINS_TEXT_SIZE = 16


class MenuPreset(NamedTuple):
    header: str
    function: Callable
