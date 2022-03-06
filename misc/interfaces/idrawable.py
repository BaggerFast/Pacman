from abc import ABC, abstractmethod
import pygame as pg


class IDrawable(ABC):
    """Interface for objects with draw functional"""
    @abstractmethod
    def process_draw(self, screen: pg.Surface) -> None:
        pass

    def additional_draw(self, screen: pg.Surface) -> None:
        pass
