from abc import abstractmethod, ABC
import pygame as pg
from misc.interfaces import ILogical, IDrawable, IEventful


class IGenericObject(IDrawable, ILogical, IEventful, ABC):
    """Interface for objects with draw, event and logical functional"""
    @abstractmethod
    def process_event(self, event: pg.event.Event) -> None:
        pass

    @abstractmethod
    def process_logic(self) -> None:
        pass

    @abstractmethod
    def process_draw(self, screen: pg.Surface) -> None:
        pass
