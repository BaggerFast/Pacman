from typing import Tuple

import pygame as pg

from misc import Font
from objects import DrawableObject


class Text(DrawableObject):
    def __init__(self, game, text: str = "",
                 size: int = 0,
                 rect: pg.Rect = pg.rect.Rect(0, 0, 0, 0),
                 color=pg.Color(255, 255, 255),
                 font=Font.DEFAULT):

        super().__init__(game)
        self.rect = rect
        self.__pos = rect
        self.size = size
        self.__color = color
        self.font = pg.font.Font(font, self.size)
        self.__text: str
        self.text = text
        self.surface: pg.Surface

    @property
    def pos(self):
        return self.__pos

    @property
    def text(self):
        return self.__text

    @property
    def color(self):
        return self.color

    @text.setter
    def text(self, text: str):
        self.__text = text if text else self.__text
        self.surface = self.font.render(self.__text, False, self.__color)
        if type(self.rect) != tuple:
            topleft = self.rect.topleft
            self.rect = self.surface.get_rect()
            self.rect.topleft = topleft

    @color.setter
    def color(self, color: pg.color):
        self.color = color
        self.surface = self.font.render(self.__text, False, self.__color)

    @pos.setter
    def pos(self, pos: Tuple[int, int]):
        self.__pos = pos

    def process_draw(self) -> None:
        self.game.screen.blit(self.surface, self.rect)

    def process_event(self, event) -> None:
        pass

    def process_logic(self) -> None:
        pass
