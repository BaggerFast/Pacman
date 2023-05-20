from pygame import Surface

from pacman.data_core.enums import RotateEnum

from .animator import Animator


class SpriteSheetAnimator(Animator):
    def __init__(self, sheet, time_step: int = 125, endless: bool = True):
        if len(sheet) < len(RotateEnum):
            raise ValueError("Len of sprite sheet is not compatible")
        self.__sheet = sheet
        self.__rotate = RotateEnum.RIGHT.value
        super().__init__(self.__sheet[RotateEnum.RIGHT.value], time_step, endless)

    # region Public

    @property
    def current_image(self) -> Surface:
        return self.__sheet[self.__rotate][self._current_index]

    def rotate(self, value) -> None:
        if abs(value) > len(RotateEnum):
            raise ValueError("Len of sprite sheet is not compatible")
        self.__rotate = abs(value)

    # endregion
