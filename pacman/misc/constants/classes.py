from abc import ABC
from typing import NamedTuple, Final

from pacman.data_core import PathManager, Dirs


# pg.mixer.Sound
class Sounds(ABC):
    CLICK: Final[str] = "navigation"
    SEED: Final[str] = "munch"
    SEED_FUN: Final[str] = "leader"
    FRUIT: Final[str] = "eat_fruit"
    GHOST: Final[str] = "eat_ghost"
    POC_INTRO: Final[str] = "pokemon_intro"
    INTERMISSION: Final[str] = "intermission"
    PELLET: Final[str] = "power_pellet"

    DEAD = PathManager.get_list_path(f"{Dirs.SOUND}/death", ext="ogg")
    GAME_OVER = PathManager.get_list_path(f"{Dirs.SOUND}/gameover", ext="ogg")
    INTRO = PathManager.get_list_path(f"{Dirs.SOUND}/intro", ext="ogg")
    SIREN = PathManager.get_list_path(f"{Dirs.SOUND}/siren", ext="ogg")


class Points:
    class Tuple(NamedTuple):
        value: int

    POINT_PER_SEED = Tuple(10).value
    POINT_PER_ENERGIZER = Tuple(50).value
    POINT_PER_FRUIT = Tuple(40).value


class Font(ABC):
    TITLE = PathManager.get_asset_path("fonts/title.ttf")
    DEFAULT = PathManager.get_asset_path("fonts/default.ttf")
    MAIN_SCENE_SIZE = 10
    BUTTON_TEXT_SIZE = 24
    BUTTON_FOR_SKINS_TEXT_SIZE = 16
    CREDITS_SCENE_SIZE = 14
