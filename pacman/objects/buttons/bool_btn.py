from typing import Callable

from pygame import Rect

from pacman.data_core import FontCfg

from .btn import Btn
from .utils import BtnColor


class BoolBtn(Btn):
    def __init__(
        self,
        text: str,
        rect: Rect,
        state: bool,
        color_true: BtnColor,
        color_false: BtnColor,
        function: Callable = None,
        select_function: Callable = None,
        text_size: int = 60,
        font: str = FontCfg.DEFAULT,
    ):
        self.__state = state
        self.__color_true = color_true
        self.__color_false = color_false
        super().__init__(text, rect, function, select_function, color_true, text_size, font)
        self.__update_color()

    def __update_color(self):
        self._set_color(self.__color_true if self.__state else self.__color_false)

    def click(self) -> None:
        super().click()
        self.__state = not self.__state
        self.__update_color()
