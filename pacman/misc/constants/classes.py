from abc import ABC

from pacman.data_core import PathUtil


class Font(ABC):
    TITLE = PathUtil.get_asset("fonts/title.ttf")
    DEFAULT = PathUtil.get_asset("fonts/default.ttf")
    MAIN_SCENE_SIZE = 10
    BUTTON_TEXT_SIZE = 24
    BUTTON_FOR_SKINS_TEXT_SIZE = 16
    CREDITS_SCENE_SIZE = 14
