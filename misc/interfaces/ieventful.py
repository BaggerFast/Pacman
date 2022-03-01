from abc import ABC, abstractmethod
import pygame as pg


class IEventful(ABC):

    @abstractmethod
    def process_event(self, event: pg.event.Event) -> None: pass

    def additional_event(self, event: pg.event.Event) -> None: pass
