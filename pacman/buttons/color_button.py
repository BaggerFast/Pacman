from typing import Union, Tuple, Callable

import pygame as pg

from misc.constants import Font
from misc.misc import Font_hint
from .button import Button
from .util import BTN_DEFAULT_COLORS, ButtonColor, BTN_GREEN_COLORS, BTN_RED_COLORS


# todo finish refactor


class ColorButton(Button):

    def __init__(self, game, text: str,
                 geometry: Union[tuple, pg.Rect],
                 status: bool,
                 function: Callable = None,
                 colors: ButtonColor = BTN_DEFAULT_COLORS,
                 center: Tuple[int, int] = None,
                 font: Font_hint = pg.font.Font(Font.DEFAULT, 24)
                 ):
        super().__init__(game, text, geometry, function, colors, center, font)
        self.status = status
        self.setup_colors()

    def setup_colors(self):
        self.colors = BTN_GREEN_COLORS if self.status else BTN_RED_COLORS

    def click(self):
        self.status = not self.status
        self.setup_colors()
        super().click()
