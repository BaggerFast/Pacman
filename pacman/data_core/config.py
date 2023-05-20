from abc import ABC
from typing import Final

from .data_classes import ResolutionSize
from .path_util import PathUtl


class Cfg(ABC):
    FPS: Final[int] = 60
    RESOLUTION: Final = ResolutionSize(224, 285)


class FontCfg(ABC):
    TITLE = PathUtl.get_asset("fonts/title.ttf")
    DEFAULT = PathUtl.get_asset("fonts/default.ttf")
    MAIN_SCENE_SIZE = 10
    BUTTON_TEXT_SIZE = 24
    BUTTON_FOR_SKINS_TEXT_SIZE = 16
    CREDITS_SCENE_SIZE = 14
