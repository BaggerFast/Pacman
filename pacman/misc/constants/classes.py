from abc import ABC
from pacman.data_core import PathManager


class Points:
    POINT_PER_SEED = 10
    POINT_PER_ENERGIZER = 50
    POINT_PER_FRUIT = 40


class Font(ABC):
    TITLE = PathManager.get_asset_path("fonts/title.ttf")
    DEFAULT = PathManager.get_asset_path("fonts/default.ttf")
    MAIN_SCENE_SIZE = 10
    BUTTON_TEXT_SIZE = 24
    BUTTON_FOR_SKINS_TEXT_SIZE = 16
    CREDITS_SCENE_SIZE = 14
