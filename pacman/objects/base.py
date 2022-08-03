import pygame as pg


class DrawableObject:

    def __init__(self, is_hidden=False) -> None:
        self.is_hidden = is_hidden
        self.rect = pg.rect.Rect(0, 0, 0, 0)

    def move(self, x, y) -> None:
        self.rect.x = x
        self.rect.y = y
        return self

    def move_center(self, x: int, y: int):
        self.rect.centerx = x
        self.rect.centery = y
        return self
