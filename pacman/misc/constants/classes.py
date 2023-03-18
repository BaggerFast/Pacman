from abc import ABC
from typing import NamedTuple

from pacman.data_core import PathManager


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
