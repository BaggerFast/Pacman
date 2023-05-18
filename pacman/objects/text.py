import pygame as pg
from pygame import Color, Rect, Surface

from pacman.data_core import Colors
from pacman.data_core.interfaces import IDrawable
from pacman.misc.constants import Font
from pacman.objects import MovementObject


class Text(MovementObject, IDrawable):
    def __init__(
        self,
        text: str,
        size: int = 0,
        rect: Rect = Rect(0, 0, 0, 0),
        color=Colors.WHITE,
        font=Font.DEFAULT,
    ):
        super().__init__()
        self.__text = ""
        self.rect = rect
        self.__color = color
        self.__font = pg.font.Font(font, size)
        self.__surface = self.__font.render(self.__text, False, self.__color)

        self.text = text

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text if text else self.__text
        self.__surface = self.__font.render(self.__text, False, self.__color)
        topleft = self.rect.topleft
        self.rect = self.__surface.get_rect()
        self.rect.topleft = topleft

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color: Color):
        self.__color = color
        self.__surface = self.__font.render(self.__text, False, self.__color)

    def draw(self, screen: Surface) -> None:
        screen.blit(self.__surface, self.rect)

    def set_alpha(self, alpha: int) -> None:
        self.__surface.set_alpha(alpha)

    def __repr__(self):
        return f"Text: {self.__text}"
