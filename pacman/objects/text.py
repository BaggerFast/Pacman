import pygame as pg
from pacman.misc.constants import Font, Color
from pacman.misc.interfaces import IDrawable
from pacman.objects.base import BaseObject


class Text(BaseObject, IDrawable):

    def __init__(self, text: str = "", size: int = 5, rect: pg.Rect = pg.rect.Rect(0, 0, 0, 0), color=Color.WHITE,
                 font=Font.DEFAULT):
        BaseObject.__init__(self)
        self.rect: pg.Rect = rect
        self.__size: int = size
        self.__color: tuple[int] = color
        self.__font = pg.font.Font(font, self.__size)

        self.__text: str = ''
        self.text: str = text

        self.__surface: pg.Surface = self.__surface_prepare()

    # region Public

    # region Implementation of IDrawable

    def process_draw(self, screen: pg.Surface) -> None:
        screen.blit(self.__surface, self.rect)

    # endregion

    # region Properties

    @property
    def text(self) -> str:
        return self.__text

    # endregion

    # region Setters

    @text.setter
    def text(self, text: str) -> None:
        self.__text = text
        self.__surface = self.__surface_prepare()

        topleft = self.rect.topleft
        self.rect = self.__surface.get_rect()
        self.rect.topleft = topleft

    # endregion

    def set_alpha(self, value: int):
        self.__surface.set_alpha(value)

    # endregion

    # region Private

    def __surface_prepare(self) -> pg.Surface:
        return self.__font.render(self.__text, False, self.__color)

    # endregion
