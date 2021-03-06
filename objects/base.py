from abc import ABC
import pygame as pg


class BaseObject(ABC):

    def __init__(self) -> None:
        # todo maybe private rect
        self.rect: pg.rect.Rect = pg.rect.Rect(0, 0, 0, 0)

    # region Public

    def move(self, x, y) -> None:
        self.rect.x = x
        self.rect.y = y

    def move_center(self, x: int, y: int) -> None:
        self.rect.centerx = x
        self.rect.centery = y

    # endregion
