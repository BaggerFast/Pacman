import pygame as pg

from pacman.misc.animator.animator import Animator


class SpriteSheetAnimator(Animator):
    def __init__(self, sheet, time_out: int = 125, repeat: bool = True):
        if len(sheet) < 4:
            raise Exception
        self.__sheet = sheet
        self.__rotate = 0
        super().__init__(self.__sheet[0], time_out, repeat)

    def rotate(self, value) -> None:
        if abs(value) > 4:
            raise Exception
        self.__rotate = abs(value)

    @property
    def current_image(self) -> pg.Surface:
        return self.__sheet[self.__rotate][self._current_index]
