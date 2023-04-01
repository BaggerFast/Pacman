from abc import ABC
import pygame as pg


class IDrawable(ABC):
    def draw(self, screen: pg.Surface) -> None:
        raise NotImplementedError

    def secondary_draw(self, screen: pg.Surface) -> None:
        pass
