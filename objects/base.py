import pygame as pg
from misc.base_pattern import BasePattern


class BaseObject(BasePattern):

    def __init__(self, game, is_hidden=False) -> None:
        self.game = game
        self.is_hidden: bool = is_hidden
        self.rect: pg.rect.Rect = pg.rect.Rect(0, 0, 0, 0)

    def move(self, x, y) -> None:
        self.rect.x = x
        self.rect.y = y

    def move_center(self, x: int, y: int) -> None:
        self.rect.centerx = x
        self.rect.centery = y
