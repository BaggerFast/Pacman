from typing import NamedTuple, Callable
import pygame as pg
from pacman.objects import ImageObject, Text


class MenuPreset(NamedTuple):
    name: str
    func: Callable


class Medal(NamedTuple):
    SPRITE: ImageObject
    TEXT: Text

    def render(self, screen: pg.Surface) -> None:
        self.SPRITE.render(screen)
        self.TEXT.render(screen)
