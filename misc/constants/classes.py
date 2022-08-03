import pygame as pg
from typing import Final
from misc.path_manager import PathManager


# todo sound

class Sounds:

    @staticmethod
    def load_list_sounds(name: str):
        return [path for path in PathManager.get_list(f'assets/sounds/{name}', ext='mp3')]

    CLICK = 'navigation.mp3'
    SEED = 'munch.mp3'
    SEED_FUN = 'leader.mp3'
    FRUIT = 'eat_fruit.mp3'
    GHOST = 'eat_ghost.mp3'
    POC_INTRO = 'pocemon_intro.mp3'
    INTERMISSION = 'intermission.mp3'
    PELLET = 'power_pellet.mp3'
    # CHEAT = load_sound('cheat.mp3')
    DEAD = 'death'
    GAMEOVER = 'gameover'
    INTRO = "intro"
    SIREN = "siren"
    # VALVE_SOUNDS = load_list_sounds('valve_skin')
    # WINDOWS_SOUNDS = load_list_sounds('windows_skin')


class Color:
    RED: Final = pg.Color(255, 0, 0)
    BLUE: Final = pg.Color(0, 0, 255)
    GREEN: Final = pg.Color(0, 255, 0)
    BLACK: Final = pg.Color(0, 0, 0)
    WHITE: Final = pg.Color(255, 255, 255)
    ORANGE: Final = pg.Color(255, 165, 0)
    YELLOW: Final = pg.Color(255, 255, 0)
    GOLD: Final = pg.Color(255, 215, 0)
    GRAY: Final = pg.Color(127, 127, 127)
    DARK_GRAY: Final = pg.Color(66, 66, 66)
    SILVER: Final = pg.Color(192, 192, 192)
    BRONZE: Final = pg.Color(205, 127, 50)
    WOODEN: Final = pg.Color(101, 67, 33)
    JET: Final = pg.Color(10, 10, 10, 120)
    MAIN_MAP: Final = pg.Color(33, 33, 255)
    DARK_RED: Final = pg.Color(125, 0, 0)
    DARK_GREEN: Final = pg.Color(0, 125, 0)
    HALF_TRANSPERENT: Final = pg.Color(0, 0, 0, 40)
    TRANSPERENT: Final = pg.Color(0, 0, 0, 0)


class Points:
    POINT_PER_SEED = 10
    POINT_PER_ENERGIZER = 50
    POINT_PER_FRUIT = 40


class Font:
    TITLE: Final = PathManager.get_asset('fonts/title.ttf')
    DEFAULT: Final = PathManager.get_asset('fonts/mono.otf')
    MAIN_SCENE_SIZE = 10
    BUTTON_TEXT_SIZE = 24
    BUTTON_FOR_SKINS_TEXT_SIZE = 16
    CREDITS_SCENE_SIZE = 14
