from typing import Final

from pacman.data_core.data_classes import ResolutionSize


class Config:
    FPS: Final[int] = 60
    RESOLUTION: Final = ResolutionSize(224, 285)
